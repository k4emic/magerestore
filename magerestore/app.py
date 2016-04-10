from .config import Config


class Magerestore:
    def __init__(self, config_file=None):
        self.config = Config()
        self.config.from_json(config_file)
