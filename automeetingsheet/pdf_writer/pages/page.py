from datetime import date
import io
from PyPDF2 import PdfReader
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas

from automeetingsheet.models.course import Course
from automeetingsheet.models.student_info import StudentInfo
from .utils import get_best_font_size

from .page_base import PageBase


# 新ページ
class Page(PageBase):
    template_file_name = "template.pdf"

    @classmethod
    def create(
        cls,
        info: StudentInfo,
        past_records: list[StudentInfo],
        deadline: date,
        rotate=False,
    ) -> "Page":
        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=landscape(A4))
        can.setFontSize(10.0)

        # 名前, 高校, 学年, 志望校の行
        y = 522
        can.setFontSize(get_best_font_size(16.0, 100, info.name))
        can.drawString(85, y, info.name)
        school_name = info.school.replace("高等学校", "")
        can.setFontSize(get_best_font_size(16.0, 100, school_name))
        can.drawString(255, y, school_name)
        can.setFontSize(16.0)
        can.drawString(388, y, info.grade)
        can.setFontSize(get_best_font_size(16.0, 380, info.univ))
        can.drawString(490, y, info.univ)

        # 今週の学習履歴
        cls.write_info_row(can, info, 436)

        # 過去の学習履歴
        base_y = 393.0
        delta_y = -20.7
        for record in cls.extract_past_records(past_records):
            cls.write_info_row(can, record, base_y)
            base_y += delta_y

        # 必要コマ数, 終了予定日
        can.setFontSize(12.0)
        y = 287.5
        can.drawString(125, y, info.finish_date)
        can.drawString(246, y, str(deadline.month))
        can.drawRightString(
            350, y, "{:.2f}".format(info.calc_weekly_required_num(deadline))
        )

        # 講座情報。
        base_y = 220
        delta_y = -16.7
        for course in cls.extract_courses(info.courses):
            cls.write_course_row(can, course, base_y)
            base_y += delta_y

        can.save()
        packet.seek(0)
        base_page = PdfReader(cls.template_file_path).pages[0]
        new_page = cls.merge(packet, base_page)
        if rotate:
            new_page.rotate(90)
        new_page.__class__ = Page
        return new_page

    @staticmethod
    def extract_courses(_courses: list[Course]) -> list[Course]:
        """
        10個までしか書けないため、完全修得ではないものを優先的に書く。
        """
        courses = [course for course in _courses if course.details != "完全修得"]
        courses += [course for course in _courses if course.details == "完全修得"]
        return courses[: min(10, len(courses))]

    @staticmethod
    def extract_past_records(_past_records: list[StudentInfo]) -> list[StudentInfo]:
        """
        5個までしか書けないため、最新のものから5つを書く。
        """
        sorted_records = sorted(
            _past_records, key=lambda x: x.created_date, reverse=True
        )
        return sorted_records[: min(5, len(sorted_records))]

    @classmethod
    def write_info_row(cls, can: canvas.Canvas, info: StudentInfo, y):
        """
        学習履歴の行を書き込む
        """
        can.setFontSize(8.0)
        can.drawCentredString(79, y, info.created_date.strftime("%Y/%m/%d"))
        can.drawCentredString(127, y, info.time)

        can.setFontSize(10.0)
        can.drawCentredString(167, y, f"{info.days}日")
        can.drawCentredString(202, y, "{:.2f}".format(info.point))

        base_x = 236.0
        delta_x = 33.4
        for value in [info.class_done, info.subtest, info.test, info.class_rest]:
            can.drawCentredString(base_x, y, str(value))
            base_x += delta_x

        can.setFontSize(8.0)
        can.drawCentredString(base_x, y, "{:.1%}".format(info.class_done_ratio))

        can.setFontSize(10.0)
        can.drawCentredString(423, y, str(info.done_english))
        can.drawCentredString(489, y, str(info.done_math))

        base_x = 539.0
        delta_x = 32.98
        master_list = info.master_list
        for i in range(len(master_list)):
            if master_list[i] is None:
                continue
            status, value = master_list[i]
            can.setFontSize(6.0)
            can.drawCentredString(base_x, y - 3, f"({status})")
            can.setFontSize(8.0)
            can.drawCentredString(base_x, y + 4, str(value))
            base_x += delta_x

    @classmethod
    def write_course_row(cls, can: canvas.Canvas, course: Course, y):
        """
        講座情報の行を書き込む
        """
        if "】" in course.title:
            course.title = course.title.split("】")[1]

        can.setFontSize(get_best_font_size(10.0, 235, course.title))

        can.drawString(59, y, course.title)
        cls.write_fraction(
            can, course.course_done_num, course.course_num, 282, y, font_size=10.0
        )
        cls.write_fraction(
            can, course.subtest_done_num, course.subtest_num, 348, y, font_size=10.0
        )
        can.setFontSize(10.0)
        delta_x = 32.98
        can.drawCentredString(404, y, "{:.1f}回".format(course.subtest_average_num))
        can.drawCentredString(439, y, str(course.subtest_ss_num))
        can.drawCentredString(439 + delta_x, y, str(course.miss_subtest_num))

        cls.write_fraction(
            can, course.test_done_num, course.test_num, 520.5, y, font_size=10.0
        )
        can.drawCentredString(572, y, str(course.test_ss_num))
        can.drawCentredString(572 + delta_x, y, str(course.test_s_num))
        can.drawCentredString(572 + 2 * delta_x, y, str(course.miss_test_num))

        can.setFontSize(get_best_font_size(8.0, 155, course.details))
        can.drawString(660, y, course.details)

    @classmethod
    def write_fraction(cls, can: canvas.Canvas, c, m, x, y, font_size):
        """
        分数をいい感じに、分母を小さく, 分子を大きく表示する
        """
        can.setFontSize(font_size)
        can.drawRightString(x, y, str(c))
        can.setFontSize(font_size - 2.0)
        can.drawString(x + 2.0, y, f"/{m}")
        can.setFontSize(font_size)


# 実際に作成できるか + 文字列が枠を越えないか テスト
if __name__ == "__main__":
    from utils import page_to_pdf
    from tests.automeetingsheet.models.get_dummy_data import get_student_info
    from page_base import TEMPLATE_DIR

    Page.create_graph_paper()

    info = get_student_info()

    # 志望校が長いとき
    info.univ = "ユニバーシティ大学 グローバルコミュニティ学部 グローバルコミュニティ学科"

    info.courses[0].title = "日本語で講座情報のタイトルがない場合にオーバーフローしないかテスト"
    info.courses[1].title = "Test for overflow when the title of the course is too long"

    # detailsが長いときにオーバーフローしないかテスト
    course = Course(
        subject="英語",
        title="long details test",
        course_num=20,
        course_done_num=20,
        subtest_num=20,
        subtest_done_num=19,
        subtest_ss_num=18,
        subtest_average_num=1.5,
        test_num=5,
        test_done_num=4,
        test_s_num=1,
        test_ss_num=0,
    )
    info.courses[2] = course

    past_records = [get_student_info() for i in range(10)]

    page = Page.create(
        info,
        past_records,
        date.today(),
    )
    page_to_pdf(page, f"{TEMPLATE_DIR}/sample/{Page.template_file_name}")
