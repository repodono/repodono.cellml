import unittest
import pkg_resources

from repodono.cellml.testing.session import FSSession


class FSSessionTestCase(unittest.TestCase):

    def test_session_object(self):
        session = FSSession(pkg_resources.resource_filename(
            'repodono.cellml.testing', 'data'))
        self.assertEqual(10, len(session._map))
        self.assertEqual(279, len(session._map[
            ('subdir1', 'subdir2', 'toplevel.xml')
        ].text))
        self.assertEqual(279, len(session.get(
            'http://example.com/subdir1/subdir2/toplevel.xml'
        ).text))
