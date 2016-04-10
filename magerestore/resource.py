class Resource:
    def __init__(self, resource_config):
        self.from_config(resource_config)

    def from_config(self, config):
        raise NotImplementedError('from_config must be implemented by subclass of Resource')


class ResourceManager:
    def __init__(self, resource_config):
        self._resources = {}
        for name, node in resource_config.items():
            self.add_resource(name, node)

    def add_resource(self, name, node_config):
        self._resources[name] = ResourceFactory.create(node_config)

    def names(self):
        """Get list of resource names"""
        return sorted([name for name in self._resources])

    def find(self, name):
        if name in self._resources:
            return self._resources[name]
        else:
            return None


class ResourceFactory:
    _factories = {}

    @staticmethod
    def add_type(name, type_class):
        ResourceFactory._factories[name] = type_class

    @staticmethod
    def create(node):
        node_type = node['type']

        if node_type not in ResourceFactory._factories:
            raise KeyError('No resource class defined for node type `{type}`'.format(type=node_type))

        type_class = ResourceFactory._factories[node_type]

        return type_class(node)
