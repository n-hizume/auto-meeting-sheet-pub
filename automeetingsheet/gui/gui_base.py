import PySimpleGUI as sg
from abc import ABCMeta, abstractmethod


# ボタンのキーを定義
class EventKey:
    OK = "ok"
    CANCEL = "cancel"
    ALL = "all"
    SOME = "some"
    FIN = "fin"
    YES = "yes"
    NO = "no"
    CLOSE = "close"
    AGAIN = "again"


class GUIBase(metaclass=ABCMeta):
    """
    ・候補１(採用)
    GUIのベースクラスを作成して、画面ごとに継承とかしてファイル, クラス単位で分ける
    - 全部をimportしないといけないのが面倒
    - 入出力で共通のインターフェースが特になく、baseを定義しにくい
    + どんなGUIが存在するのか一目でわかる
    + 画面ごとにファイルを分けることで、ファイルが肥大化しない

    ・候補2
    候補1を呼び出すhandle classを作る
    + importが楽
    - いちいち登録しないといけない
    - ymlとかで書いたら全読み込みできるが、動的に作りづらい(生徒数とか不定なので)

    ・候補3
    一つのクラスに、各GUIをclass methodとして持たせる
    - コードが長くなる
    - どんなGUIが存在するのか読まないとわからない
    + importが楽
    + 動的に作れる
    + 一元管理できる
    """

    @staticmethod
    def _extract_event_key(layout) -> list[EventKey]:
        res = []
        for row in layout:
            for element in row:
                if isinstance(element, sg.Button):
                    res.append(element.key)
        return res

    @classmethod
    def _show(cls, title, layout) -> tuple[EventKey, any]:
        window = sg.Window(title, layout)
        event_key_list = cls._extract_event_key(layout)

        while True:
            event, values = window.read()
            if event == sg.WIN_CLOSED:
                window.close()
                return EventKey.CLOSE, None

            elif event in event_key_list:
                window.close()
                return event, values

    @classmethod
    @abstractmethod
    def show(cls):
        raise NotImplementedError
