import PySimpleGUI as sg
from automeetingsheet.gui.gui_base import GUIBase, EventKey


class SelectGroupGUI(GUIBase):
    """
    グループ一覧から、グループを選択してもらうGUI
    全生徒を印刷するか、一部生徒を印刷するか、終了するかを選択できるため、
    ボタンの内容(EventKey)と、選択したグループ名を返す。
    """

    @classmethod
    def show(cls, group_list: list[str]) -> tuple[EventKey, str | None]:
        title = "グループ選択画面"
        layout = [
            [sg.Text("グループを選択してください")],
            [sg.Combo(group_list, size=(15, 7), default_value=group_list[0])],
            [
                sg.Button("全生徒を印刷する", key=EventKey.ALL),
                sg.Button("一部生徒を印刷する", key=EventKey.SOME),
                sg.Button("終了", key=EventKey.FIN),
            ],
        ]

        event, values = cls._show(title, layout)
        if event == EventKey.ALL:
            return EventKey.ALL, values[0]
        elif event == EventKey.SOME:
            return EventKey.SOME, values[0]
        elif event == EventKey.FIN:
            return EventKey.FIN, None

        return None, None


if __name__ == "__main__":
    res = SelectGroupGUI.show(["A", "B", "C"])
    print(res)
