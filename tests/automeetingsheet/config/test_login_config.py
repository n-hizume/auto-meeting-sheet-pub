from unittest import TestCase
from unittest.mock import patch, MagicMock
from automeetingsheet.config.login_config import LoginConfig


# JSONファイルをreadする時のMockの返り値
def get_return_value():
    return {
        "id": "id",
        "password": "password",
        "school": "school",
        "deadline12": "2000/01/01",
        "deadline3": "2000/01/01",
        "year": "2000",
        "is_old_sheet": True,
    }


class TestLoginConfig(TestCase):
    # 正常にReadできるか
    def test_read(self):
        with patch("json.load", MagicMock(return_value=get_return_value())):
            config = LoginConfig.read()
        self.assertIsInstance(config, LoginConfig)
        self.assertEqual(config.__dict__, get_return_value())

    # 日付が無効な表記の時に正しくvalidateで弾かれるか
    def test_read_invalid_deadline(self):
        value = get_return_value()
        value["deadline12"] = "2000/01/0"
        with patch("json.load", MagicMock(return_value=value)):
            with self.assertRaises(ValueError):
                LoginConfig.read()
