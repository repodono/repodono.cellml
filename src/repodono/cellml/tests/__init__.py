# -*- coding: utf-8 -*-
import unittest
from os.path import dirname


def make_suite():  # pragma: no cover
    test_loader = unittest.TestLoader()
    test_suite = test_loader.discover(
        'repodono.cellml.tests', pattern='test_*.py',
        top_level_dir=dirname(__file__),
    )
    return test_suite
