import unittest
import os
from magerestore.config import Config


class ConfigTest(unittest.TestCase):

    def test_from_json(self):
        config = Config()
        config.from_json(os.path.join(os.path.dirname(__file__), 'static', 'config.json'))

        self.assertTrue('sample' in config.repos, 'sample repo is seen in repo config')
        self.assertEqual(len(config.repos), 1, 'only one sample repo')

        self.assertTrue('mysql' in config.resources, 'mysql resource found')
        self.assertTrue('media' in config.resources, 'media resource found')
