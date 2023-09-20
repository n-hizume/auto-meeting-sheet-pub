import PySimpleGUI as sg
from automeetingsheet.gui.gui_base import GUIBase, EventKey


class SelectSchoolGUI(GUIBase):
    """
    校舎一覧から後者を選択してもらうGUI
    Login時に存在しない校舎を入力した場合に使用する。
    """

    @classmethod
    def show(cls, invalid_school: str, school_list: list[str]) -> str | None:
        title = "校舎選択画面"
        layout = [
            [sg.Text(f"「{invalid_school}」という名前の校舎は選択できません。")],
            [sg.Text("校舎を以下から選択してください")],
            [
                sg.Combo(
                    school_list,
                    size=(15, 7),
                    default_value=school_list[0],
                    readonly=True,  # 書き換え不可にする
                )
            ],
            [sg.Button("決定", key=EventKey.OK)],
        ]

        event, values = cls._show(title, layout)
        if event == EventKey.OK:
            return values[0]


if __name__ == "__main__":
    res = SelectSchoolGUI.show("A", ["B", "C", "D"])
    print(res)
