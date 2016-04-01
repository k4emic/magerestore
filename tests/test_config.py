import unittest
import os
from magerestore.config import Config


def get_static_file_path(filename):
    return os.path.join(os.path.dirname(__file__), 'static', filename)


class ConfigTest(unittest.TestCase):

    def test_from_json(self):
        config = Config()
        config.from_json(get_static_file_path('config.json'))

        self.assertTrue('sample' in config.repos, 'sample repo is seen in repo config')
        self.assertEqual(len(config.repos), 1, 'only one sample repo')

        self.assertTrue('mysql' in config.resources, 'mysql resource found')
        self.assertTrue('media' in config.resources, 'media resource found')
