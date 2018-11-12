import unittest
import pkg_resources

from repodono.cellml.model import ModelLoader
from repodono.cellml.testing.session import FSSession


class ModelLoaderTestCase(unittest.TestCase):

    def setUp(self):
        self.loader = ModelLoader(FSSession(pkg_resources.resource_filename(
            'repodono.cellml.testing', 'data')))

    def assertComponentName(self, componentSet, name):
        comp = componentSet.getComponent(name)
        self.assertEqual(comp.name, name)

    def test_unicode_issues(self):
        # since requests.session ensures that text is returned with any
        # input that cannot be converted be replaced with a replacement
        # character (U+FFFD), both following targets should produce a
        # model.
        valid = self.loader('http://example.com/unicode_valid.cellml')
        invalid = self.loader('http://example.com/unicode_invalid.cellml')
        self.assertEqual(valid.cmetaId, 'unicode_valid')
        self.assertEqual(invalid.cmetaId, 'unicode_invalid')

    def test_model_load_multiple_import(self):
        model = self.loader('http://example.com/multiimport.xml')
        isi = model.imports.iterateImports()
        v1 = isi.nextImport().importedModel
        v2 = isi.nextImport().importedModel

        self.assertComponentName(model.modelComponents, 'component1')
        self.assertComponentName(model.modelComponents, 'component2')

        self.assertComponentName(v1.modelComponents, 'level1_component')
        self.assertComponentName(v2.modelComponents, 'level2_component')
