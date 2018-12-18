import logging

try:
    from urllib.parse import urljoin
except ImportError:  # pragma: no cover
    from urlparse import urljoin

import requests

from repodono.cellml.bootstrap import cellml

logger = logging.getLogger(__name__)


class ModelLoader(object):

    def __init__(self, roots=()):
        self.roots = roots

    def _load(self, model_loader, target):
        for root in self.roots:
            try:
                raw = root.text(target)
            except Exception:  # TODO find better identifier
                continue
            else:
                return model_loader(raw)

        raise ValueError("'%s' cannot be loaded" % target)

    def __call__(self, target):

        def queue_incoming(base, model):
            # need to remember the source that this import was derived
            # from; use the xml:base of the model if available.
            base_url = model.xmlBase.asText or base
            subimports = model.imports
            incoming_models.append((base_url, subimports,))

        incoming_models = []
        model = self._load(cellml.modelLoader.createFromText, target)
        queue_incoming(target, model)

        while len(incoming_models):
            base, imports = incoming_models.pop(0)
            for imp in imports:
                relurl = imp.xlinkHref.asText
                # note: <https://bugs.python.org/issue18828>, if custom
                # session object is provided for the support of schemas
                # other than the default ones.
                nexturl = urljoin(base, relurl)
                self._load(imp.instantiateFromText, nexturl)
                queue_incoming(nexturl, imp.importedModel)

        return model


class RequestsModelLoader(object):

    def __init__(self, session=requests.Session()):
        self.session = session

    def __call__(self, target):

        def queue_incoming(base, model):
            # need to remember the source that this import was derived
            # from; use the xml:base of the model if available.
            base_url = model.xmlBase.asText or base
            subimports = model.imports
            incoming_models.append((base_url, subimports,))

        incoming_models = []
        model_string = self.session.get(target).text
        model = cellml.modelLoader.createFromText(model_string)
        queue_incoming(target, model)

        while len(incoming_models):
            base, imports = incoming_models.pop(0)
            for imp in imports:
                relurl = imp.xlinkHref.asText
                # note: <https://bugs.python.org/issue18828>, if custom
                # session object is provided for the support of schemas
                # other than the default ones.
                nexturl = urljoin(base, relurl)
                source = self.session.get(nexturl).text
                imp.instantiateFromText(source)
                queue_incoming(nexturl, imp.importedModel)

        return model
