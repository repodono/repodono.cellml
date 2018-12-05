import unittest
import pkg_resources
import ast

from repodono.cellml.model import ModelLoader
from repodono.cellml.codegen import default_codegen

from repodono.cellml.testing.session import FSSession


class CodeGenTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = ModelLoader(FSSession(pkg_resources.resource_filename(
            'repodono.cellml.testing', 'data')))
        self.codegen = default_codegen()

    def test_code_gen_basic(self):
        model = self.loader('http://example.com/beeler_reuter_1977.cellml')
        results = self.codegen(model)
        # currently only 5 included celeds definition.
        self.assertEqual(5, len(results))
        self.assertTrue(isinstance(ast.parse(results['Python']), ast.Module))
