from unittest import TestCase
from tests.automeetingsheet.models.get_dummy_data import get_student_info

from automeetingsheet.database.student_info_entity import StudentInfoEntity


class TestStudentInfoEntity(TestCase):
    # modelの型からの変換で特にエラーが起きない
    def test_from_model(self):
        student_info = get_student_info()
        student_info_entity = StudentInfoEntity.from_model(student_info)
        self.assertIsInstance(student_info_entity, StudentInfoEntity)
        self.assertEqual(student_info_entity.kiso_1200, "完全修得,1200")

    # entityに変換したのをmodel型に戻すと完全に元に戻るか確認。Optionalの値は消えることに注意
    def test_to_model(self):
        student_info = get_student_info()
        student_info_entity = StudentInfoEntity.from_model(student_info)
        student_info_restore = student_info_entity.to_model()

        # delete optional properties
        student_info.school = ""
        student_info.univ = ""
        student_info.grade = ""
        student_info.href = ""
        student_info.courses = []

        self.assertEqual(student_info, student_info_restore)
