import os
from collections import namedtuple
from os.path import (
    join,
    sep,
)
from urllib.parse import urlparse

FSResponse = namedtuple('FSResponse', ['text'])


class FSSession(object):

    def __init__(self, datapath):
        dpidx = len(datapath.split(sep))
        self._map = {}
        for datasubpath, _, filenames in os.walk(datapath):
            root = datasubpath.split(sep)[dpidx:]
            for fn in filenames:
                with open(join(datasubpath, fn), errors="replace") as fd:
                    self._map[tuple(root + [fn])] = FSResponse(fd.read())

    def get(self, target, *a, **kw):
        return self._map[tuple(urlparse(target).path.split('/')[1:])]
