from unittest import TestCase
from unittest.mock import patch, MagicMock
from automeetingsheet.config.env_config import EnvConfig


# JSONファイルをreadする時のMockの返り値
def get_return_value():
    return {
        "proxy": "proxy",
    }


class TestLoginConfig(TestCase):
    # 正しくReadできるか
    def test_read(self):
        with patch("json.load", MagicMock(return_value=get_return_value())):
            config = EnvConfig.read()
        self.assertIsInstance(config, EnvConfig)
        self.assertEqual(config.__dict__, get_return_value())
