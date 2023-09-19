from datetime import date
from unittest import TestCase
from unittest.mock import MagicMock, patch
from .get_dummy_data import get_student_info


class TestStudentInfo(TestCase):
    # 各@propertyが正しい値になっているか
    def test_properties(self):
        info = get_student_info()
        self.assertEqual(info.class_done_ratio, 0.8)
        self.assertEqual(
            info.master_list,
            [
                ("完全修得", 1200),
                ("完全修得", 1800),
                ("完全修得", 750),
                ("完全修得", 750),
                ("完全修得", 100),
                ("完全修得", 100),
                ("完全修得", 100),
                None,
            ],
        )

    @patch(
        "automeetingsheet.models.student_info.get_today",
        MagicMock(return_value=date(2021, 1, 1)),
    )
    def test_calc_weekly_required_num(self):
        info = get_student_info()
        # 7days, 10 class -> 10.0
        self.assertAlmostEqual(info.calc_weekly_required_num(date(2021, 1, 7)), 10.0)
        # 1days, 10 class -> 70.0
        self.assertAlmostEqual(info.calc_weekly_required_num(date(2021, 1, 1)), 70.0)
        # 0 days, 10 class -> 10.0(=rest)
        self.assertAlmostEqual(info.calc_weekly_required_num(date(2020, 12, 31)), 10.0)

    @patch(
        "automeetingsheet.models.student_info.get_today",
        MagicMock(return_value=date(2021, 1, 1)),
    )
    def test_finish_date(self):
        info = get_student_info()

        # 修了済
        info.class_rest = 0
        info.class_done = 0
        self.assertEqual(info.finish_date, "修了済")

        # 丁度修了
        info.class_done = 1
        self.assertEqual(info.finish_date, "修了済")

        # 受講数0
        info.class_rest = 1
        info.class_done = 0
        self.assertEqual(info.finish_date, "∞")

        # あと1週間
        info.class_rest = 7
        info.class_done = 7
        self.assertEqual(info.finish_date, "2021/01/08")

        # あと1日
        info.class_rest = 1
        self.assertEqual(info.finish_date, "2021/01/02")

        # あと0日
        info.class_done = 20
        self.assertEqual(info.finish_date, "2021/01/01")
