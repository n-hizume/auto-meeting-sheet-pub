from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from datetime import date, timedelta

from automeetingsheet.models.student_info import StudentInfo
from automeetingsheet.database.student_info_entity import StudentInfoEntity, engine


class StudentInfoHandler:
    """
    DBの操作を行うクラス
    引数や返り値は全て汎用インターフェースで行い、内部でDBのEntityと相互変換する。
    TODO:
        実使用するDBをうまくMockできない構造で、テストを書きにくい。
        テスト用のDBファイルを作成できるような構造にしたい。
    """

    @staticmethod
    def insert_records(students: list[StudentInfo]):
        """
        リストで受け取り一括でDBにInsert
        """
        student_entities = [StudentInfoEntity.from_model(s) for s in students]
        session = sessionmaker(bind=engine)()
        session.add_all(student_entities)
        session.commit()
        session.close()

    @staticmethod
    def delete_old_records(days: int):
        """
        手動版TTL。定期的に古いデータを削除する。
        """
        session = sessionmaker(bind=engine)()
        session.query(StudentInfoEntity).filter(
            StudentInfoEntity.created_date < (date.today() - timedelta(days=days))
        ).delete()
        session.commit()
        session.close()

    @staticmethod
    def get_records(name: str, num: int) -> list[StudentInfo]:
        """
        特定の生徒の最新のデータを{num}件取得する。今日insertしたデータも変えることに注意
        TODO: Optional引数で、今日を含めるか指定
        """
        session = sessionmaker(bind=engine)()
        records = (
            session.query(StudentInfoEntity)
            .filter(StudentInfoEntity.name == name)
            .order_by(desc(StudentInfoEntity.created_date))
            .limit(num)
            .all()
        )
        session.close()

        return [r.to_model() for r in records]
