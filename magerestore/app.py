from .config import Config
from .resource import ResourceManager


class Magerestore:
    def __init__(self, config_file=None):
        self.config = Config()
        self.config.from_json(config_file)
        self.resources = ResourceManager(self.config.resources)
