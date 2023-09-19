from abc import ABCMeta, abstractmethod
import json


class ConfigBase(metaclass=ABCMeta):
    __config_folder_path: str = "config/"
    config_file_name: str = None

    @abstractmethod
    def __init__(self, config):
        pass

    @classmethod
    @property
    def __config_file_path(cls):
        """
        継承先の設定値と親ディレクトリを合わせて、JSONファイルのパスを返す。
        """
        if cls.config_file_name is None:
            raise NotImplementedError("cls.config_file_nameが設定されていません。")
        return cls.__config_folder_path + cls.config_file_name

    @staticmethod
    @abstractmethod
    def validate_config(config):
        pass

    @classmethod
    def read(cls):
        """
        JsonからのFactory関数
        ファイルの形式が正しいかのvalidateも同時に行う
        """
        with open(cls.__config_file_path, encoding="utf-8") as f:
            config = json.load(f)
        cls.validate_config(config)
        return cls(config)

    def write(self):
        """
        現在の値をJsonに書き込む
        書き込む前にvalidateも行う
        """
        config = self.__dict__
        self.validate_config(config)
        with open(self.__config_file_path, "w", encoding="utf-8") as f:
            json.dump(config, f, indent=4, ensure_ascii=False)
