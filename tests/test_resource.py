import unittest
from magerestore.resource import ResourceFactory, ResourceManager


class MockResourceType:
    def __init__(self, config):
        self.config = config


ResourceFactory.add_type('mock', MockResourceType)


class ResourceFactoryTest(unittest.TestCase):
    def test_add_type(self):
        node = dict(type='mock')
        resource = ResourceFactory.create(node)
        self.assertTrue(isinstance(resource, MockResourceType))


class ResourceManagerTest(unittest.TestCase):

    SAMPLE_NODES = dict(
        foo=dict(type='mock'),
        bar=dict(type='mock')
    )

    def setUp(self):
        self.manager = ResourceManager(self.SAMPLE_NODES)

    def test_names(self):
        self.assertEqual(self.manager.names(), ['bar', 'foo'])

    def test_find(self):
        self.manager.add_resource('special name', dict(type='mock'))
        self.assertIsNotNone(self.manager.find('special name'))
        self.assertIsNotNone(self.manager.find('foo'))
        self.assertIsNone(self.manager.find('doesnt exist'))
