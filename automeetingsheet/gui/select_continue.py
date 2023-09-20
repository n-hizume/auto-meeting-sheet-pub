import PySimpleGUI as sg
from automeetingsheet.gui.gui_base import GUIBase, EventKey


class SelectContinueGUI(GUIBase):
    """
    続けるかを選択してもらうだけのGUI
    """

    @classmethod
    def show(cls) -> bool:
        title = "続けますか？"
        layout = [
            [sg.Text("続けて生徒を選択しますか？(グループ選択画面に戻ります)")],
            [sg.Button("はい", key=EventKey.YES), sg.Button("いいえ", key=EventKey.NO)],
        ]

        event, _ = cls._show(title, layout)
        return True if event == EventKey.YES else False


if __name__ == "__main__":
    is_continue = SelectContinueGUI.show()
    print(is_continue)
