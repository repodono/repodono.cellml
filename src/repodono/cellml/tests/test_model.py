import unittest
import pkg_resources

from repodono.task.root import FSRoot
from repodono.task.root import RequestsRoot

from repodono.cellml.model import ModelLoader
from repodono.cellml.model import RequestsModelLoader
from repodono.cellml.testing.session import FSSession


class TestCase(unittest.TestCase):

    def assertComponentName(self, componentSet, name):
        comp = componentSet.getComponent(name)
        self.assertEqual(comp.name, name)


class RequestsModelLoaderTestCase(TestCase):

    def setUp(self):
        self.loader = RequestsModelLoader(
            FSSession(pkg_resources.resource_filename(
                'repodono.cellml.testing', 'data')))

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


class ModelLoaderTestCase(TestCase):

    def setUp(self):
        self.root = FSRoot(pkg_resources.resource_filename(
            'repodono.cellml.testing', 'data'))

    def test_single_loader_various(self):
        loader = ModelLoader([self.root])
        self.assertEqual(
            'unicode_valid', loader('unicode_valid.cellml').cmetaId)
        self.assertEqual(
            'unicode_valid', loader('/unicode_valid.cellml').cmetaId)
        self.assertEqual(
            'unicode_valid', loader('../unicode_valid.cellml').cmetaId)

    def test_single_loader_imports(self):
        loader = ModelLoader([self.root])
        model = loader('multiimport.xml')
        isi = model.imports.iterateImports()
        v1 = isi.nextImport().importedModel
        v2 = isi.nextImport().importedModel

        self.assertComponentName(model.modelComponents, 'component1')
        self.assertComponentName(model.modelComponents, 'component2')

        self.assertComponentName(v1.modelComponents, 'level1_component')
        self.assertComponentName(v2.modelComponents, 'level2_component')

    def test_single_loader_imports_missing(self):
        loader = ModelLoader([self.root])
        with self.assertRaises(ValueError):
            loader('multiimport_absolute.cellml')

    def test_multi_loader_imports_missing(self):
        requests_root = RequestsRoot(FSSession(pkg_resources.resource_filename(
            'repodono.cellml.testing', 'data')))
        loader = ModelLoader([self.root, requests_root])
        # the http method now supported
        model = loader('multiimport_absolute.cellml')
        self.assertComponentName(model.modelComponents, 'component1')
        self.assertComponentName(model.modelComponents, 'component2')

    def test_single_loader_missing(self):
        loader = ModelLoader([self.root])
        with self.assertRaises(ValueError):
            loader('nosuchmodel.cellml')
