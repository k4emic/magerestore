import os
import unittest
from magerestore.repository import RepositoryFactory, RepositoryManager, SFTPRepository


class MockRepository:
    def __init__(self, **config):
        self.config = config


class MockRepositoryFoo:
    def __init__(self, **config):
        self.config = config


class RepositoryFactoryTest(unittest.TestCase):

    def test_add_type(self):
        factory = RepositoryFactory()
        factory.add_type('mock', MockRepository)
        self.assertTrue('mock' in factory.types)

    def test_create(self):

        factory = RepositoryFactory()
        # type must be declared before trying to use
        with self.assertRaises(KeyError):
            repo_config = dict(type='mock')
            factory.create(repo_config)

        factory.add_type('mock', MockRepository)
        repo_config = dict(type='mock')
        repo = factory.create(repo_config)
        self.assertIsInstance(repo, MockRepository)

        factory.add_type('mock_foo', MockRepositoryFoo)
        repo_config = dict(type='mock_foo')
        repo = factory.create(repo_config)
        self.assertIsInstance(repo, MockRepositoryFoo)


class RepositoryManagerTest(unittest.TestCase):

    def test_get_repo(self):
        repo_config = dict(
            mock=dict(type='mock')
        )
        manager = RepositoryManager(repo_config)
        manager.factory.add_type('mock', MockRepository)
        mock_repo = manager.get_repo('mock')
        self.assertIsInstance(mock_repo, MockRepository)


class SFTPRepositoryTest(unittest.TestCase):

    ENV_KEY_HOST = 'MAGERESTORE_TEST_SFTP_HOSTNAME'
    ENV_KEY_FILEPATH = 'MAGERESTORE_TEST_SFTP_REMOTEFILE'

    def test_get_file(self):
        host = os.environ.get(self.ENV_KEY_HOST)
        filepath = os.environ.get(self.ENV_KEY_FILEPATH)
        if not host:
            self.fail('No hostname specified for SFTP get_file test')

        repo = SFTPRepository(host=host)
        temp_file = repo.get_file(filepath)
        size = os.path.getsize(temp_file.name)
        self.assertGreater(size, 5000)
