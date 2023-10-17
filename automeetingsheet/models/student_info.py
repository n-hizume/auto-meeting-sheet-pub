from datetime import date, timedelta
from typing import Tuple
from dataclasses import dataclass, field
from .course import Course

TODAY = date.today()


# テストで日付をMockできるように関数化
def get_today():
    return TODAY


@dataclass
class StudentInfo:
    """
    生徒情報の汎用インターフェース
    生徒テーブルのページから取得できる値と生徒詳細ページから取得できる値に分かれているため、
    いくつかのプロパティはOptional。
    TODO:
    - Optionalをまとめる。
    - Master用の型定義
    """

    created_date: date
    name: str
    point: float  # 向上得点
    class_rest: int  # 残り受講数
    class_total: int  # 合計受講数

    class_done: int  # 今週の受講数
    subtest: int  # 今週の確認テスト数
    test: int  # 今週の中間・修了テスト数

    days: int  # 週の登校日数
    time: str  # 週の在校時間

    # --- 高速マスター　--- TODO: 取ってない場合にNoneにするの、インターフェースがゴチャつきそう
    done_english: int  # 週の英語マスターをやった回数
    done_math: int  # 週の数学マスターをやった回数
    kiso_1200: Tuple[str, int] | None  # 基礎単語1200 (<状況>, <実施数>)
    center_1800: Tuple[str, int] | None  # センター英単語1800
    jukugo_750: Tuple[str, int] | None  # 英熟語750
    bunpo_750: Tuple[str, int] | None  # 英文法750
    math1: Tuple[str, int] | None  # 数学１
    mathA: Tuple[str, int] | None  # 数学A
    math2: Tuple[str, int] | None  # 数学２
    mathB: Tuple[str, int] | None  # 数学B

    # DBには保存しないプロパティ(Optional)
    school: str = ""
    univ: str = ""
    grade: str = ""
    href: str = ""
    courses: list[Course] = field(default_factory=lambda: [])

    def __str__(self) -> str:
        return self.name

    # 受講率(max1.0)
    @property
    def class_done_ratio(self) -> float:
        return (
            0.0
            if self.class_total == 0
            else self.class_total / (self.class_total + self.class_rest)
        )

    # 受講期限を守るためには週何コマ受講が必要か
    def calc_weekly_required_num(self, deadline: date) -> float:
        rest_days = (deadline - get_today()).days + 1
        # 期限を過ぎている場合、残り受講数を返す
        if rest_days <= 0:
            return self.class_rest
        return self.class_rest / (rest_days / 7.0)

    # このペースで行くといつ受講が終わるか
    @property
    def finish_date(self) -> str:
        if self.class_rest == 0:
            return "修了済"
        if self.class_done == 0:
            return "∞"

        required_days = int((self.class_rest / self.class_done) * 7)
        return (get_today() + timedelta(days=required_days)).strftime("%Y/%m/%d")

    # for文で回せるように、リストの形のプロパティを用意
    @property
    def master_list(self) -> list[Tuple[str, int] | None]:
        return [
            self.kiso_1200,
            self.center_1800,
            self.jukugo_750,
            self.bunpo_750,
            self.math1,
            self.mathA,
            self.math2,
            self.mathB,
        ]
