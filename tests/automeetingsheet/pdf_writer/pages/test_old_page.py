from datetime import date, timedelta
from unittest import TestCase
from automeetingsheet.pdf_writer.pages.old_page import OldPage
from tests.automeetingsheet.models.get_dummy_data import get_student_info, get_course


class TestOldPage(TestCase):
    # createでエラーが起きないか確認
    def test_create(self):
        page = OldPage.create(get_student_info(), date.today())
        self.assertIsInstance(page, OldPage)

    # 講座の抽出(順番, 個数)
    def test_extract_courses(self):
        courses = [get_course(is_perfect=True) for i in range(100)]

        # 確認テスト残り100
        courses[5].title = "A"
        courses[5].test_num = 50
        courses[5].test_done_num = 50
        courses[5].test_ss_num = 50
        courses[5].subtest_num = 100
        courses[5].subtest_done_num = 100
        courses[5].subtest_ss_num = 0

        # 確認テスト残り100, 修了テスト残り50
        courses[10].title = "B"
        courses[10].test_num = 50
        courses[10].test_done_num = 50
        courses[10].test_ss_num = 0
        courses[10].subtest_num = 100
        courses[10].subtest_done_num = 100
        courses[10].subtest_ss_num = 0

        # 修了テスト1つ受けていない
        courses[15].title = "C"
        courses[15].test_num = 100
        courses[15].test_done_num = 99
        courses[15].test_ss_num = 99

        # 残り97こは完全修得

        extracted_courses = OldPage.extract_post_courses(courses)

        self.assertEqual(len(extracted_courses), 3)
        self.assertEqual(
            [course.title for course in extracted_courses], ["B", "C", "A"]
        )

        # 大量にあっても、4こまでしか表示されない
        for i in range(50, 100):
            courses[i].subtest_ss_num -= 1
        extracted_courses = OldPage.extract_post_courses(courses)
        self.assertEqual(len(extracted_courses), 4)
