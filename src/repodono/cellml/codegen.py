import logging
import pkg_resources
from os.path import (
    join,
    splitext,
)
# from os import listdir
from repodono.cellml.bootstrap import (
    # cellml,
    celedsexporter,
)

logger = logging.getLogger(__name__)


class CodeGenerator(object):

    def __init__(self, celeds_map=()):
        self.exporters = {}
        for key, definition in celeds_map:
            self.exporters[key] = celedsexporter.createExporterFromText(
                definition)

    def __call__(self, model):
        results = {}
        for key, exporter in self.exporters.items():
            results[key] = exporter.generateCode(model)
        return results


def default_codegen():
    rootdir = pkg_resources.resource_filename(
        'repodono.cellml', join('resource', 'celeds'))
    celeds_names = [
        'C_IDA.xml', 'C.xml', 'F77.xml', 'MATLAB.xml', 'Python.xml']
    celeds_map = []

    for name in celeds_names:
        with open(join(rootdir, name)) as fd:
            celeds_map.append((splitext(name)[0], fd.read()))

    return CodeGenerator(celeds_map)
