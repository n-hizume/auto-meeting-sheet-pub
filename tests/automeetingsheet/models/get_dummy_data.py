from automeetingsheet.models.course import Course
from automeetingsheet.models.student_info import StudentInfo, TODAY

"""
テスト用に適当なダミーデータを返す。
"""


def get_student_info() -> StudentInfo:
    return StudentInfo(
        created_date=TODAY,
        name="山田 太郎",
        point=10.0,
        class_rest=10,
        class_total=40,
        class_done=1,
        subtest=1,
        test=0,
        days=7,
        time="10時間10分",
        done_english=100,
        done_math=100,
        kiso_1200=("完全修得", 1200),
        center_1800=("完全修得", 1800),
        jukugo_750=("完全修得", 750),
        bunpo_750=("完全修得", 750),
        math1=("完全修得", 100),
        mathA=("完全修得", 100),
        math2=("完全修得", 100),
        mathB=None,
        school="帝丹高等学校",
        univ="京都大学 工学部 情報学科",
        grade="高3",
        href="https://www.hoge.com/",
        courses=[get_course() for i in range(10)],
    )


def get_course(is_perfect=False) -> Course:
    course = Course(
        subject="英語",
        title="リスニング",
        course_num=20,
        course_done_num=15,
        subtest_num=20,
        subtest_done_num=14,
        subtest_ss_num=10,
        subtest_average_num=1.5,
        test_num=5,
        test_done_num=4,
        test_s_num=1,
        test_ss_num=1,
    )

    # 完全修得Ver
    if is_perfect:
        course.course_done_num = course.course_num
        course.subtest_done_num = course.subtest_num
        course.subtest_ss_num = course.subtest_num
        course.test_done_num = course.test_num
        course.test_ss_num = course.test_num
        course.test_s_num = 0

    return course
