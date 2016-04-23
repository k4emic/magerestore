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

        return cls._types[repo_type](config)


class RepositoryManager:

    factory = RepositoryFactory

    def __init__(self, repo_config=None):
        self.repositories = {}
        if repo_config is not None:
            for name, config in repo_config.items():
                self.from_config(name, config)

    def add_repo(self, name, repo_config):
        self.repositories[name] = self.factory.create(repo_config)
