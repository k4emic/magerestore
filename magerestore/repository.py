import paramiko
import os
import tempfile


class RepositoryFactory:

    _types = dict()

    @classmethod
    def add_type(cls, name, repository_cls):
        cls._types[name] = repository_cls

    @classmethod
    def create(cls, config):
        repo_type = config['type']
        if repo_type not in cls._types:
            raise KeyError("Not a valid repository type: `{type}`".format(type=repo_type))

        return cls._types[repo_type](**config)


class RepositoryManager:

    factory = RepositoryFactory

    def __init__(self, repo_config=None):
        self.repositories = {}
        if repo_config is not None:
            for name, config in repo_config.items():
                self.add_repo(name, config)

    def add_repo(self, name, repo_config):
        self.repositories[name] = self.factory.create(repo_config)


class SFTPRepository:
    def __init__(self, host=None, port=None, user=None, password=None, description=None, type=None):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.description = description
        self.type = type
        self.ssh_config_file = os.path.expanduser('~/.ssh/config')

    def get_file(self, remote_file, progress_callback=None):

        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh_config = paramiko.SSHConfig()
        if os.path.exists(self.ssh_config_file):
            with open(self.ssh_config_file) as ssh_config_file:
                ssh_config.parse(ssh_config_file)

        connection_config = dict(
            hostname=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
        )

        # mapping between internal config and ssh config files
        user_config_mapping = dict(
            hostname='hostname',
            username='user',
            port='port',
            key_filename='identityfile'
        )

        user_config = ssh_config.lookup(self.host)

        for connection_name, user_name in user_config_mapping.items():
            if user_name in user_config:
                connection_config[connection_name] = user_config[user_name]

        # strip keys with None as value to fall back on defaults in paramiko
        empty_keys = [key for key, value in connection_config.items() if value is None]
        for key in empty_keys:
            del connection_config[key]

        ssh.connect(**connection_config)
        sftp = ssh.open_sftp()
        temp_file = self.get_temp_file()
        sftp.get(remote_file, temp_file.name, progress_callback)

        # ensure contents are written to disk
        temp_file.flush()
        os.fsync(temp_file)

        return temp_file

    def get_temp_file(self):
        return tempfile.NamedTemporaryFile()

RepositoryFactory.add_type('sftp', SFTPRepository)
