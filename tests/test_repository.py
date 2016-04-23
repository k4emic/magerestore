import unittest
from magerestore.repository import RepositoryFactory, RepositoryManager


class MockRepository:
    def __init__(self, config):
        self.config = config


class MockRepositoryFoo:
    def __init__(self, config):
        self.config = config


class MockRepositoryFactory(RepositoryFactory):
    @classmethod
    def create(cls, config):
        return config


class RepositoryFactoryTest(unittest.TestCase):

    def tearDown(self):
        RepositoryFactory._types = dict()

    def test_add_type(self):
        RepositoryFactory.add_type('mock', MockRepository)
        self.assertTrue('mock' in RepositoryFactory._types)

    def test_create(self):
        # type must be declared before trying to use
        with self.assertRaises(KeyError):
            repo_config = dict(type='mock')
            RepositoryFactory.create(repo_config)

        RepositoryFactory.add_type('mock', MockRepository)
        repo_config = dict(type='mock')
        repo = RepositoryFactory.create(repo_config)
        self.assertIsInstance(repo, MockRepository)

        RepositoryFactory.add_type('mock_foo', MockRepositoryFoo)
        repo_config = dict(type='mock_foo')
        repo = RepositoryFactory.create(repo_config)
        self.assertIsInstance(repo, MockRepositoryFoo)


class RepositoryManagerTest(unittest.TestCase):

    def test_add_repo(self):
        repo_config = dict(
            type='mock'
        )
        manager = RepositoryManager()
        manager.factory = MockRepositoryFactory()
        manager.add_repo('mock', repo_config)
        self.assertTrue('mock' in manager.repositories)
        self.assertEqual(manager.repositories['mock'], repo_config)