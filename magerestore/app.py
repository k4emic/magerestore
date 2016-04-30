from magerestore.config import Config
from magerestore.resource import ResourceManager
from magerestore.repository import RepositoryManager


class Magerestore:
    def __init__(self, config_file=None):
        self.config = Config()
        self.config.from_json(config_file)
        self.repo_manager = RepositoryManager(self.config.repos)
        self.resource_manager = ResourceManager(self.config.resources, self.repo_manager)
