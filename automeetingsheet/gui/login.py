import PySimpleGUI as sg
from automeetingsheet.gui.gui_base import GUIBase, EventKey
from automeetingsheet.config.login_config import LoginConfig


class LoginGUI(GUIBase):
    """
    ログイン時に初期情報を入力するGUI
    LoginConfigと内容を同期し、変更があれば上書きする。
    validateに失敗した場合、エラーを出す。
    """

    @classmethod
    def show(cls) -> LoginConfig | None:
        login_config = LoginConfig.read()
        title = "ログイン画面"
        layout = [
            [sg.Text("ID: ", size=(10, 1)), sg.InputText(login_config.id)],
            [sg.Text("Password: ", size=(10, 1)), sg.InputText(login_config.password)],
            [sg.Text("校舎: ", size=(10, 1)), sg.InputText(login_config.school)],
            [
                sg.Text("高1,2受講終了日: ", size=(10, 1)),
                sg.InputText(login_config.deadline12),
            ],
            [sg.Text("高3受講終了日: ", size=(10, 1)), sg.InputText(login_config.deadline3)],
            [sg.Text("年度: ", size=(10, 1)), sg.InputText(login_config.year)],
            [
                sg.Checkbox(
                    "旧ミーティングシートを出力", size=(35, 7), default=login_config.is_old_sheet
                )
            ],
            [sg.Button("ログイン", key=EventKey.OK)],
        ]

        event, values = cls._show(title, layout)
        if event == EventKey.OK:
            login_config.id = values[0]
            login_config.password = values[1]
            login_config.school = values[2]
            login_config.deadline12 = values[3]
            login_config.deadline3 = values[4]
            login_config.year = values[5]
            login_config.is_old_sheet = values[6]

            LoginConfig.validate_config(login_config.__dict__)
            login_config.write()
            return login_config

        return None


if __name__ == "__main__":
    res = LoginGUI.show()
    print(res)
