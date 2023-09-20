from datetime import date, timedelta
from unittest import TestCase
from automeetingsheet.pdf_writer.pages.page import Page
from tests.automeetingsheet.models.get_dummy_data import get_student_info, get_course


class TestPage(TestCase):
    # createでエラーが起きないか確認
    def test_create(self):
        page = Page.create(get_student_info(), [get_student_info()] * 10, date.today())
        self.assertIsInstance(page, Page)

    # 講座の抽出(順番, 個数)
    def test_extract_courses(self):
        # 20個に1個未修得の講座一覧
        courses = [get_course(is_perfect=i % 20 != 0) for i in range(100)]

        # 最初の５個は未修得, 後ろ五個は完全修得になるはず
        extracted_courses = Page.extract_courses(courses)
        self.assertEqual(len(extracted_courses), 10)
        details_list = [course.details for course in extracted_courses]
        self.assertEqual(details_list.count("完全修得"), 5)
        self.assertEqual(details_list[5:], ["完全修得"] * 5)

        # 一個の場合
        courses = [get_course()]
        extracted_courses = Page.extract_courses(courses)
        self.assertEqual(len(extracted_courses), 1)

        # 0この場合
        courses = []
        extracted_courses = Page.extract_courses(courses)
        self.assertEqual(len(extracted_courses), 0)

    # 過去記録の抽出(日付順, 個数)
    def test_extract_past_records(self):
        past_records = [get_student_info() for i in range(10)]
        for i, info in enumerate(past_records):
            info.created_date = date(2020, 1, 1) + timedelta(days=i)

        extracted_records = Page.extract_past_records(past_records)
        self.assertEqual(len(extracted_records), 5)
        self.assertEqual(extracted_records[0].created_date, date(2020, 1, 10))
        self.assertEqual(extracted_records[-1].created_date, date(2020, 1, 6))

        # 一個の場合
        extracted_records = Page.extract_past_records(past_records[:1])
        self.assertEqual(len(extracted_records), 1)

        # 0この場合
        extracted_records = Page.extract_past_records([])
        self.assertEqual(len(extracted_records), 0)
