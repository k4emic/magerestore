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
