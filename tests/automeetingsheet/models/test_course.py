from unittest import TestCase
from .get_dummy_data import get_course


class TestCourse(TestCase):
    # 各@propertyが正しい値になっているか
    def test_properties(self):
        course = get_course()

        self.assertEqual(course.miss_subtest_num, 4)
        self.assertEqual(course.miss_test_num, 3)

    # detailsに間違いがないか
    def test_details(self):
        course = get_course()
        details = course.details.split(",")
        self.assertEqual(set(details), {"確テSS未満アリ", "修テSS未満アリ", "確テ未受験アリ"})

        # 確認テストを全て受験
        course.subtest_done_num = 15
        details = course.details.split(",")
        self.assertEqual(set(details), {"確テSS未満アリ", "修テSS未満アリ"})

        # 確認テスト全て合格
        course.subtest_ss_num = 15
        details = course.details.split(",")
        self.assertEqual(set(details), {"修テSS未満アリ"})

        # 修了テスト全て合格
        course.test_s_num = 0
        course.test_ss_num = 4
        self.assertEqual(course.details, "")

        # 受講・確認テスト・テスト全て完了
        course.course_done_num = 20
        course.subtest_done_num = 20
        course.subtest_ss_num = 20
        course.test_done_num = 5
        course.test_ss_num = 5
        self.assertEqual(course.details, "完全修得")

        # 修了テスト一つSS逃す
        course.test_ss_num = 4
        self.assertEqual(course.details, "修テSS未満アリ")
        course.test_ss_num = 5

        # 確認テスト一つSS逃す
        course.subtest_ss_num = 19
        self.assertEqual(course.details, "確テSS未満アリ")

        # 確認テスト一つ受験しない
        course.subtest_done_num = 19
        self.assertEqual(course.details, "確テ未受験アリ")

        # 受講と確認テストの総数が違う場合、割合で判定
        course.course_num = 20
        course.course_done_num = 10
        course.subtest_num = 10
        course.subtest_done_num = 5
        self.assertNotIn("確テ未受験アリ", course.details)

        course.subtest_done_num = 4
        self.assertIn("確テ未受験アリ", course.details)

        # 過去問など、受講数が0の場合
        course.course_num = 0
        self.assertEqual(course.details, "")
