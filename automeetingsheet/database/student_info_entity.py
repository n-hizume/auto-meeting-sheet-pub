import sqlalchemy
from sqlalchemy import Column, Integer, String, Float, Date, PrimaryKeyConstraint
from sqlalchemy.orm import declarative_base
from datetime import date
from typing import Tuple

from automeetingsheet.models.student_info import StudentInfo

TODAY = date.today()

DATABASE_FILE_PATH = "database/student_info_db.sqlite3"

engine = sqlalchemy.create_engine(f"sqlite:///{DATABASE_FILE_PATH}", echo=False)
Base = declarative_base()


class StudentInfoEntity(Base):
    """
    DBのEntityスキーマ定義
    インターフェースはStudentInfoと酷似しているが、依存関係を減らすために別で定義。
    """

    __tablename__ = "StudentInfo"

    created_date = Column(Date)  # TIMESTAMP(作成日)
    name = Column(String(length=20))  # 生徒名

    point = Column(Float)  # 向上得点
    class_rest = Column(Integer)  # 残り受講数
    class_total = Column(Integer)  # 合計受講数
    class_done = Column(Integer)  # 受講済み講数

    subtest = Column(Integer)  # 確認テスト合格数
    test = Column(Integer)  # 中間・修了テスト合格数

    days = Column(Integer)  # 登校日数
    time = Column(String(20))  # 登校時間

    done_english = Column(Integer)  # 高マス英語クリック数
    done_math = Column(Integer)  # 高マス数学問題数

    # 高速マスター
    kiso_1200 = Column(String(20))  # 基礎1200
    center_1800 = Column(String(20))  # センター1800
    jukugo_750 = Column(String(20))  # 英熟語750
    bunpo_750 = Column(String(20))  # 英文法750
    math1 = Column(String(20))  # 数学Ⅰ
    mathA = Column(String(20))  # 数学A
    math2 = Column(String(20))  # 数学Ⅱ
    mathB = Column(String(20))  # 数学B

    # 主Keyは(日付, 名前)。同じ日付のデータは同じはずなので、衝突が起きた場合は特に上書きしない。
    PrimaryKeyConstraint(created_date, name, sqlite_on_conflict="IGNORE")

    def __str__(self):
        return self.name

    @classmethod
    def from_model(cls, info: StudentInfo) -> "StudentInfoEntity":
        """
        modelのインターフェースからDBのEntityへの変換。
        modelの型の方が汎用インターフェースなので、database moduleに閉じるべき。
        TODO: 動的なvalidate(引数の省略など) initを用意するか、dataclassと組み合わせたい。
        """
        return cls(
            created_date=info.created_date,
            name=info.name,
            point=info.point,
            class_rest=info.class_rest,
            class_total=info.class_total,
            class_done=info.class_done,
            subtest=info.subtest,
            test=info.test,
            days=info.days,
            time=info.time,
            done_english=info.done_english,
            done_math=info.done_math,
            kiso_1200=cls.__parse_master_pair(info.kiso_1200),
            center_1800=cls.__parse_master_pair(info.center_1800),
            jukugo_750=cls.__parse_master_pair(info.jukugo_750),
            bunpo_750=cls.__parse_master_pair(info.bunpo_750),
            math1=cls.__parse_master_pair(info.math1),
            mathA=cls.__parse_master_pair(info.mathA),
            math2=cls.__parse_master_pair(info.math2),
            mathB=cls.__parse_master_pair(info.mathB),
        )

    def to_model(self) -> StudentInfo:
        """
        汎用インターフェースへの変換
        """
        return StudentInfo(
            created_date=self.created_date,
            name=self.name,
            point=self.point,
            class_rest=self.class_rest,
            class_total=self.class_total,
            class_done=self.class_done,
            subtest=self.subtest,
            test=self.test,
            days=self.days,
            time=self.time,
            done_english=self.done_english,
            done_math=self.done_math,
            kiso_1200=self.__parse_master_str(self.kiso_1200),
            center_1800=self.__parse_master_str(self.center_1800),
            jukugo_750=self.__parse_master_str(self.jukugo_750),
            bunpo_750=self.__parse_master_str(self.bunpo_750),
            math1=self.__parse_master_str(self.math1),
            mathA=self.__parse_master_str(self.mathA),
            math2=self.__parse_master_str(self.math2),
            mathB=self.__parse_master_str(self.mathB),
        )

    @staticmethod
    def __parse_master_str(s: str) -> Tuple[str, int] | None:
        if len(s) < 2:
            return None
        pair = s.split(",")
        return (pair[0], int(pair[1]))

    @staticmethod
    def __parse_master_pair(pair: Tuple[str, int] | None) -> str:
        if pair is None:
            return ""
        return f"{pair[0]},{pair[1]}"


Base.metadata.create_all(bind=engine)
