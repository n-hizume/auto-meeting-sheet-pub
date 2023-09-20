from datetime import datetime
import os

from PyPDF2 import PdfWriter
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

from automeetingsheet.config.login_config import LoginConfig
from automeetingsheet.models.student_info import StudentInfo
from automeetingsheet.pdf_writer.pages.page import Page
from automeetingsheet.pdf_writer.pages.old_page import OldPage


# フォントの設定
MS = "C:\Windows\Fonts/msgothic.ttc"
FONT = "MS P Gothic"
if os.path.exists(MS):
    pdfmetrics.registerFont(TTFont(FONT, MS))
else:
    pdfmetrics.registerFont(UnicodeCIDFont("HeiseiKakuGo-W5"))
    FONT = "HeiseiKakuGo-W5"


# PDF書き込みのためのhandlerクラス
class PDFWriter:
    # LoginConfigに、締切や年度, PDFの種類などの情報が入っているのでそのまま受け取る
    def __init__(self, config: LoginConfig):
        self.config = config
        self.output = PdfWriter()
        self.deadline12 = datetime.strptime(config.deadline12, "%Y/%m/%d").date()
        self.deadline3 = datetime.strptime(config.deadline3, "%Y/%m/%d").date()

    # ある生徒の本日の情報と過去の記録を受け取り、PDFにページを追加する
    def add_student(self, student_info: StudentInfo, past_records: list[StudentInfo]):
        deadline = self.deadline3 if student_info.grade == "高3" else self.deadline12
        if self.config.is_old_sheet:
            self.output.add_page(OldPage.create(student_info, deadline))
            self.output.add_page(
                Page.create(student_info, past_records, deadline, rotate=True)
            )
        else:
            self.output.add_page(Page.create(student_info, past_records, deadline))

    # PDFを保存する
    def save(self, file_path: str):
        with open(file_path, "wb") as f:
            self.output.write(f)


# 実際に作成できるかテスト
if __name__ == "__main__":
    from tests.automeetingsheet.models.get_dummy_data import get_student_info

    config = LoginConfig.read()
    writer = PDFWriter(config)
    for i in range(5):
        writer.add_student(get_student_info(), [get_student_info()] * 10)

    writer.save(f"output/test.pdf")
