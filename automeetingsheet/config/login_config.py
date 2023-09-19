from datetime import datetime

from config_base import ConfigBase


class LoginConfig(ConfigBase):
    config_file_name = "login_config.json"

    def __init__(self, config):
        self.id: str = config["id"]
        self.password: str = config["password"]
        self.school: str = config["school"]
        self.deadline12: str = config["deadline12"]
        self.deadline3: str = config["deadline3"]
        self.year: str = config["year"]
        self.is_old_sheet: bool = config["is_old_sheet"]

    @staticmethod
    def validate_config(config):
        # propertyの存在確認. initでどのみちエラーになるが、validate関数内でエラーを出して欲しい
        for key in [
            "id",
            "password",
            "school",
            "deadline12",
            "deadline3",
            "year",
            "is_old_sheet",
        ]:
            if not key in config:
                raise KeyError(f"{key}が存在しません。")

        # str型確認
        for key in ["id", "password", "school"]:
            if not isinstance(config[key], str):
                raise TypeError(f"{key}の型がstrではありません。")

        # bool型確認
        for key in ["is_old_sheet"]:
            if not isinstance(config[key], bool):
                raise TypeError(f"{key}の型がboolではありません。")

        # 日付形式確認
        for key in ["deadline12", "deadline3"]:
            try:
                datetime.strptime(config[key], "%Y/%m/%d")
            except:
                raise ValueError(f"{key}は、'2000/01/01'のような形式で入力してください。")

        # 年度の形式確認
        try:
            datetime.strptime(config["year"], "%Y")
        except:
            raise ValueError(f'yearは、"2000"のように西暦で入力してください。')


if __name__ == "__main__":
    config = LoginConfig.read()
