import PySimpleGUI as sg
from automeetingsheet.gui.gui_base import GUIBase, EventKey
import traceback


class ErrorGUI(GUIBase):
    """
    エラー発生時に表示するGUI
    """

    @classmethod
    def show(
        cls, title="警告", text="予期せぬエラーが発生しました。もう一度やり直してください。", enable_again=False
    ) -> EventKey:
        buttons = [sg.Button("閉じる", key=EventKey.CLOSE)]
        if enable_again:
            buttons.insert(0, sg.Button("やり直す", key=EventKey.AGAIN))
        layout = [[sg.Text(text)], buttons]

        res, _ = cls._show(title, layout)
        return res

    @classmethod
    def show_by_error(cls, e: Exception):
        """
        Exceptionを受け取って、エラー内容を表示する。
        """
        error_code = e.__class__.__name__
        error_message = traceback.format_exception_only(type(e), e)[0].strip()

        cls.show(
            "エラーが発生しました",
            "\n".join(
                [
                    "エラーが発生しました。もう一度やり直してください。",
                    f"エラーコード: {error_code}",
                    f"エラーメッセージ: {error_message}",
                ]
            ),
        )


if __name__ == "__main__":
    try:
        raise ValueError("test raise error")
    except Exception as e:
        ErrorGUI.show_by_error(e)
