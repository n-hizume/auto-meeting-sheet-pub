from .config_base import ConfigBase


class EnvConfig(ConfigBase):
    config_file_name = "env_config.json"

    def __init__(self, config):
        self.proxy: str = config["proxy"]

    @staticmethod
    def validate_config(config):
        if not isinstance(config["proxy"], str):
            raise TypeError(f"proxyの型がstrではありません。")
