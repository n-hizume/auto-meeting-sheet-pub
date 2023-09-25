from datetime import date
import datetime
import io
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from automeetingsheet.models.course import Course

from automeetingsheet.models.student_info import StudentInfo
from automeetingsheet.pdf_writer.pages.page_base import PageBase, FONT_NAME
from automeetingsheet.pdf_writer.pages.utils import get_best_font_size


TODAY = date.today()


# 旧ページ
class OldPage(PageBase):
    template_file_name = "old_template.pdf"

    @classmethod
    def create(cls, info: StudentInfo, deadline: date) -> "OldPage":
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=A4)
        can.setFont(FONT_NAME, 10.0)
        can.setFontSize(10.0)

        # 名前, 高校, 学年, 志望校の行
        y = 805
        can.setFontSize(14)
        can.drawCentredString(90, y, TODAY.strftime("%Y/%m/%d"))
        can.setFontSize(get_best_font_size(16.0, 75, info.name))
        can.drawString(192, y, info.name)
        school_name = info.school.replace("高等学校", "")
        can.setFontSize(get_best_font_size(16.0, 75, school_name))
        can.drawString(323, y, school_name)
        can.setFontSize(14)
        can.drawString(444, y, info.grade)

        # 今週の受講・テスト実績の列
        x = 525
        base_y = 686
        delta_y = -32
        can.setFontSize(14)
        can.drawCentredString(x, base_y, str(info.subtest))
        can.drawCentredString(x, base_y + delta_y, str(info.test))
        can.drawCentredString(x, base_y + delta_y * 2, str(info.class_rest))
        can.drawCentredString(
            x, base_y + delta_y * 3, "{:.1%}".format(info.class_done_ratio)
        )

        # 受講コマ, 必要コマ/週
        can.setFontSize(16)
        can.drawCentredString(x, 764, str(info.class_done))
        can.drawCentredString(
            x, 725, "{:.1f}".format(info.calc_weekly_required_num(deadline))
        )

        # 必要コマ/週の文章
        can.setFontSize(7.5)
        can.drawCentredString(x, 748, f"{deadline.month}月末受講終了には")

        # 受講終了予定日
        can.setFontSize(get_best_font_size(14, 50, info.finish_date[2:]))
        can.drawCentredString(x, 558, info.finish_date[2:])

        y = 508
        # 在校時間
        can.setFontSize(get_best_font_size(16.0, 120, info.time))
        can.drawCentredString(88, y, info.time)

        # 在校日数
        can.setFontSize(
            get_best_font_size(
                18.0,
                100,
                f"{info.days}日",
            )
        )
        can.drawCentredString(192, y, f"{info.days}日")

        # 向上得点
        can.setFontSize(18.0)
        can.drawCentredString(283, y, str(info.point))

        # 日付の行
        week_index = TODAY.weekday()
        for i in range(7):
            delta = i - week_index
            if delta <= 0:
                delta += 7
            this_day = TODAY + datetime.timedelta(days=delta)
            day = this_day.day
            can.drawCentredString(160 + i * 51, 774, str(day))

        # 高速マスター
        can.setFontSize(16.0)
        can.drawCentredString(272, 457, str(info.done_english))
        can.drawCentredString(500, 457, str(info.done_math))
        cls.write_master_table(can, info.master_list)

        # テストを受けるべき講座のテーブル
        y = 290
        delta_y = -24.0
        courses = cls.extract_post_courses(info.courses)
        for course in courses:
            cls.write_course_row(can, course, y)
            y += delta_y

        can.save()
        packet.seek(0)
        base_page = PdfReader(cls.template_file_path).pages[0]

        new_page = cls.merge(packet, base_page)
        new_page.__class__ = OldPage
        return new_page

    @staticmethod
    def extract_post_courses(
        _courses: list[Course],
    ) -> list[Course]:
        """
        テストなどが残っている講座の抽出
        TODO: 先にテスト数でfilterした方が高速？サイズによるかも
        """

        if len(_courses) == 0:
            return []

        # (テストが残っている順, 確認テストが残っている順) にsort
        courses = sorted(
            _courses,
            key=lambda x: (x.miss_test_num + x.ignore_test_num, x.miss_subtest_num),
            reverse=True,
        )

        # 最大４つまで かつ、テストが残っていない講座は不要
        size = min(4, len(courses))
        for i in range(size):
            if (
                courses[i].miss_test_num
                + courses[i].ignore_test_num
                + courses[i].miss_subtest_num
                == 0
            ):
                size = i
                break
        return courses[:size]

    @classmethod
    def write_master_table(cls, can: canvas.Canvas, master_list):
        """
        マスターのテーブルに書き込み
        """
        can.setFontSize(10.0)
        x_list = [216, 295, 420, 511]
        y_list = [438, 425, 410, 397]
        for i in range(len(master_list)):
            if master_list[i] is None:
                continue
            status, num = master_list[i]
            y = y_list[i // 2]
            x1 = x_list[i % 2 * 2]
            x2 = x_list[i % 2 * 2 + 1]
            can.drawCentredString(x1, y, status)
            can.drawCentredString(x2, y, str(num))

    @classmethod
    def write_course_row(cls, can: canvas.Canvas, course: Course, y):
        """
        講座のテーブルに書き込み
        """
        if "】" in course.title:
            course.title = course.title.split("】")[1]
        can.setFontSize(get_best_font_size(10.0, 195, course.title))
        can.drawString(42, y, course.title)
        can.setFontSize(10.0)
        can.drawCentredString(267, y, str(course.miss_subtest_num))
        can.drawCentredString(
            318, y, str(course.miss_test_num + course.ignore_test_num)
        )


# 実際に作成できるか + 文字列が枠を越えないか テスト
if __name__ == "__main__":
    from utils import page_to_pdf
    from page_base import TEMPLATE_DIR
    from tests.automeetingsheet.models.get_dummy_data import get_student_info

    OldPage.create_graph_paper()

    info = get_student_info()
    info.courses[0].title = "日本語で講座情報のタイトルがない場合にオーバーフローしないかテスト"
    info.courses[1].title = "Test for overflow when the title of the course is too long"
    page = OldPage.create(
        info,
        date.today(),
    )
    page_to_pdf(page, f"{TEMPLATE_DIR}/sample/{OldPage.template_file_name}")
