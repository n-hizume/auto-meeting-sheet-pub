import PySimpleGUI as sg
from automeetingsheet.gui.gui_base import GUIBase, EventKey


class SelectStudentsGUI(GUIBase):
    """
    印刷する生徒をチェックボックスから選択してもらうGUI
    dict(key: グループ名, value: 生徒名のリスト)を受け取り、順そのままのboolのリストを返す。
    """

    @classmethod
    def show(
        cls, group_dict: dict[str, list[str]], default: bool = False
    ) -> list[bool]:
        title = "生徒選択画面"
        layout = [
            [sg.Text("印刷する生徒を選択してください(複数選択可)")],
        ]
        for group_name in group_dict:
            student_name_list: list = group_dict[group_name]
            layout.append([sg.Text(f"■{group_name}")])
            layout.extend(
                [
                    [sg.Checkbox(student_name, size=(35, 7), default=default)]
                    for student_name in student_name_list
                ]
            )

        layout.append(
            [sg.Button("選択", key=EventKey.OK), sg.Button("キャンセル", key=EventKey.CANCEL)]
        )

        event, values = cls._show(title, layout)
        if event == EventKey.OK:
            return list(values.values())
        else:
            return []


if __name__ == "__main__":
    res = SelectStudentsGUI.show(
        {
            "group1": ["name1", "name2", "name3"],
            "group2": ["name4", "name5", "name6"],
        },
        True,
    )
    print(res)
