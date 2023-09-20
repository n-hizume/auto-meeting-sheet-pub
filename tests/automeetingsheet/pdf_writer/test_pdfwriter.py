from unittest import TestCase
from automeetingsheet.config.login_config import LoginConfig
from automeetingsheet.pdf_writer.pdf_writer import PDFWriter

from tests.automeetingsheet.models.get_dummy_data import get_student_info


class TestPDFWriter(TestCase):
    def test_create(self):
        """
        createでエラーが起きないか確認。
        save後のレイアウトはテストの範疇を超えるため特に確かめない。
        """
        config = LoginConfig(
            {
                "id": "test",
                "password": "test",
                "school": "test",
                "deadline12": "2025/01/01",
                "deadline3": "2025/01/01",
                "year": "2025",
                "is_old_sheet": True,
            }
        )

        writer = PDFWriter(config)
        for _ in range(5):
            writer.add_student(get_student_info(), [get_student_info()] * 10)

        self.assertEqual(len(writer.output.pages), 10)

        config.is_old_sheet = False
        writer = PDFWriter(config)
        for _ in range(5):
            writer.add_student(get_student_info(), [get_student_info()] * 10)

        self.assertEqual(len(writer.output.pages), 5)
