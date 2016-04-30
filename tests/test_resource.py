import unittest
from magerestore.resource import ResourceFactory, ResourceManager


class MockResourceType:
    def __init__(self, config, manager):
        self.config = config


class ResourceFactoryTest(unittest.TestCase):
    def test_add_type(self):
        factory = ResourceFactory(None)
        factory.add_type('mock', MockResourceType)
        self.assertTrue('mock' in factory.types)

    def test_create(self):
        factory = ResourceFactory(None)
        # type must be declared before trying to use
        with self.assertRaises(KeyError):
            resource_config = dict(type='mock')
            factory.create(resource_config)

        factory.add_type('mock', MockResourceType)
        resource_config = dict(type='mock')
        repo = factory.create(resource_config)
        self.assertIsInstance(repo, MockResourceType)

        factory.add_type('mock_foo', MockResourceType)
        resource_config = dict(type='mock_foo')
        repo = factory.create(resource_config)
        self.assertIsInstance(repo, MockResourceType)


class ResourceManagerTest(unittest.TestCase):

    SAMPLE_NODES = dict(
        foo=dict(type='mock'),
        bar=dict(type='mock')
    )

    def setUp(self):
        self.manager = ResourceManager(self.SAMPLE_NODES, None)
        self.manager.factory.add_type('mock', MockResourceType)

    def test_names(self):
        self.assertEqual(self.manager.names(), ['bar', 'foo'])

    def test_get_resource(self):
        self.assertIsInstance(self.manager.get_resource("foo"), MockResourceType)
        self.assertIsInstance(self.manager.get_resource("bar"), MockResourceType)
