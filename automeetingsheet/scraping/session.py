import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import os
from automeetingsheet.models.student_info import StudentInfo
from automeetingsheet.scraping.parse_entity import (
    parse_basic_student_info,
    parse_optional_student_info,
)
from automeetingsheet.scraping.utils import strip


# URL管理
class URL:
    LOGIN = "https://<<secret>>"
    SECRET = "https://<<secret>>"


class WebSession:
    def __init__(self, proxy: str = None):
        # プロキシ設定
        if proxy is not None:
            os.environ["http_proxy"] = proxy
            os.environ["httsp_proxy"] = proxy
        self.session = requests.Session()

        # これがないとうまく動かない
        self.session.headers.update(
            {
                # secret
            }
        )

        self.group_href_dict = dict([])
        self.response = None
        # self.get(URL.LOGIN)

    # 現在のURLを取得
    @property
    def current_url(self) -> str:
        if self.response is None:
            raise ValueError("No response.")
        return self.response.url

    # 現在のページをparse用の型に変換して取得
    def get_parser(self) -> BeautifulSoup:
        if self.response is None:
            raise ValueError("No response.")
        return BeautifulSoup(self.response.text, "html.parser")

    # GETしてresponseを格納
    def get(self, url: str):
        self.response = self.session.get(url)

    # POST {data} してresponseを格納
    def post(self, url: str, data: dict[str, any]):
        self.response = self.session.post(url, data=data)

    # 現在のURLが正しいか確認。特定のページにいる時だけ呼ばれるはずの関数などで使用
    # boolを返してもいいが、どうせ毎回raiseするのでここでraiseしてvoidを返す。
    def check_current_url(
        self,
        ideal_url: str,
        ignore_query: bool = False,
        error_msg: str = "URL Location is wrong.",
    ):
        current_url = self.current_url

        # クエリの消去
        if ignore_query:
            ideal_url = ideal_url.split("?")[0]
            current_url = current_url.split("?")[0]

        # 大文字小文字を区別しない
        current_url = current_url.lower()
        ideal_url = ideal_url.lower()

        # 最後のスラッシュを消す
        if current_url[-1] == "/":
            current_url = current_url[:-1]
        if ideal_url[-1] == "/":
            ideal_url = ideal_url[:-1]

        if current_url != ideal_url:
            raise ValueError(
                f"{error_msg}\nideal: '{ideal_url}'\ncurrent: '{current_url}'"
            )

    # ログイン
    def login(self, id, pwd):
        # secret
        pass

    # 校舎一覧の画面に移動し、校舎名のリストを取得
    def get_school_list(self) -> list[str]:
        # secret
        return []

    # 校舎を選択し、その校舎のページに移動
    def select_school(self, school_name: str):
        # secret
        pass

    # グループ一覧の画面に移動し、グループ名のリストを取得
    def get_group_list(self) -> list[str]:
        # secret
        return []

    # グループを選択してそのグループのページに移動 + 生徒情報の取得 + グループ一覧に戻る
    def get_student_info_list(self, group_name: str) -> list[StudentInfo]:
        # secret
        return []

    # StundentInfo.href のページに移動し、生徒の詳細情報をStudentInfoに追加
    def add_students_detail(self, students: list[StudentInfo]):
        # secret
        pass


if __name__ == "__main__":
    session = WebSession()
    session.login("***", "***")
    schools = session.get_school_list()
    session.select_school("****")
    groups = session.get_group_list()
    students = session.get_student_info_list("****")
    students += session.get_student_info_list("******")
    session.add_students_detail(students)
    print(students[0])
