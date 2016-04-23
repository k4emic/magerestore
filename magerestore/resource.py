import paramiko
import tempfile
import subprocess


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


class MagentoDatabaseResource:
    def __init__(self, config):
        self.path = config['path']
        self.repository = config['repo']
        self.temp_file = tempfile.NamedTemporaryFile(delete=False)
        self.steps = [{
            'title': 'Downloading mysqldump',
            'method': self.get_file
        },
        {
            'title': 'Importing dump',
            'method': self.import_dump
        }]

    def get_file(self):
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(self.repository['host'], port=self.repository['port'])
        sftp = ssh.open_sftp()
        remotepath = self.path
        localpath = self.temp_file.name
        sftp.get(remotepath, localpath)
        self.localpath = localpath

    def import_dump(self):
        args = ['n98-magerun.phar', 'db:import', '--drop', '--compression=gzip', '--drop', '--', self.localpath]
        print(args)
        pid = subprocess.Popen(args)

ResourceFactory.add_type('magento_database', MagentoDatabaseResource)
