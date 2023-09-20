from unittest import TestCase
import PySimpleGUI as sg

from automeetingsheet.gui.gui_base import GUIBase, EventKey


# TODO: base以外にも何かしらテストができると嬉しい。現在は各GUIはクラス定義を実行することで動作確認
class TestGuiBase(TestCase):
    # layoutから、EventKeyを抽出するテスト
    def test_extract_event_key(self):
        layout = [
            [sg.Text("a")],
            [sg.Button("all", key=EventKey.ALL)],
            [sg.Button("some", key=EventKey.SOME)],
            [
                sg.Button("ok", key=EventKey.OK),
                sg.Button("cancel", key=EventKey.CANCEL),
            ],
        ]

        res = GUIBase._extract_event_key(layout)
        self.assertEqual(
            res, [EventKey.ALL, EventKey.SOME, EventKey.OK, EventKey.CANCEL]
        )
