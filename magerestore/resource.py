import subprocess


class ResourceManager:
    def __init__(self, resource_config, repo_manager):
        self.repo_manager = repo_manager
        self.resources = {}
        for name, node in resource_config.items():
            self.add_resource(name, node)

    def add_resource(self, name, node_config):
        self.resources[name] = ResourceFactory.create(node_config, self)

    def names(self):
        """Get list of resource names"""
        return sorted([name for name in self.resources])

    def find(self, name):
        if name in self.resources:
            return self.resources[name]
        else:
            return None


class ResourceFactory:
    _factories = {}

    @staticmethod
    def add_type(name, type_class):
        ResourceFactory._factories[name] = type_class

    @staticmethod
    def create(node, resource_manager):
        node_type = node['type']

        if node_type not in ResourceFactory._factories:
            raise KeyError('No resource class defined for node type `{type}`'.format(type=node_type))

        type_class = ResourceFactory._factories[node_type]

        return type_class(node, resource_manager)


class MagentoDatabaseResource:
    def __init__(self, config, resource_manager):
        self.path = config['path']
        self.manager = resource_manager

    def get_resource(self, progress_callback=None):
        return self.repository.get_file(self.path, progress_callback)

    def import_resource(self):
        args = ['n98-magerun.phar', 'db:import', '--drop', '--compression=gzip', '--drop', '--', self.localpath]
        proc = subprocess.Popen(args)

    def cleanup(self):
        pass

ResourceFactory.add_type('magento_database', MagentoDatabaseResource)
