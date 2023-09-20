from bs4 import BeautifulSoup
from datetime import date
from automeetingsheet.scraping.utils import strip

from automeetingsheet.models.student_info import StudentInfo
from automeetingsheet.models.course import Course

TODAY = date.today()


def parse_basic_student_info(row1: BeautifulSoup, row2: BeautifulSoup) -> StudentInfo:
    """
    生徒情報が載った行を受け取り、StudentInfoにparseして返す。
    """
    # secret
    pass


def parse_optional_student_info(info: StudentInfo, detail_page: BeautifulSoup):
    """
    StudentInfoに詳細情報をparseして追加する。
    """
    # secret
    pass


def parse_course(course_row: BeautifulSoup) -> Course:
    """
    講座情報が載った行を受け取り、Courseにparseして返す。
    """
    # secret
    pass
