from unittest import TestCase

from automeetingsheet.scraping.session import WebSession


class TestSession(TestCase):
    def test_current_url(self):
        url = "https://www.google.com/"
        session = WebSession()
        session.get(url)
        self.assertEqual(session.current_url, url)

    def test_current_url(self):
        url = "https://www.google.com/"
        session = WebSession()
        session.get(url)
        self.assertEqual(session.check_current_url(url), None)
        # スラッシュなし
        self.assertEqual(session.check_current_url("https://www.google.com"), None)

        # 大文字あり, クエリあり
        url_query = "https://www.Google.com/?q=python"
        session.get(url_query)
        self.assertEqual(session.check_current_url(url, ignore_query=True), None)

        # クエリによるエラー
        with self.assertRaises(ValueError):
            session.check_current_url(url, ignore_query=False)
