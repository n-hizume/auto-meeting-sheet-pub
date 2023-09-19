from dataclasses import dataclass


@dataclass
class Course:
    """
    講座に関する汎用インターフェース
    少しPDF用に寄せすぎているため、PDF用のインターフェースを別で定義して切り離したさがある。
    """

    subject: str  # 科目
    title: str  # 講座名
    course_num: int  # 講座数
    course_done_num: int  # 受講済み講座数
    subtest_num: int  # 確認テスト数
    subtest_done_num: int  # 受験済み確認テスト数
    subtest_ss_num: int  # 確認テストSS数
    subtest_average_num: float  # 確認テスト平均受験数
    test_num: int  # 中間・修了テスト数
    test_done_num: int  # 受験済み中間・修了テスト数
    test_s_num: int  # 中間・修了テストS数
    test_ss_num: int  # 中間・修了テストSS数

    def __str__(self):
        return f"【{self.subject}】{self.title}"

    # SS未満の確認テスト数
    @property
    def miss_subtest_num(self):
        return self.subtest_done_num - self.subtest_ss_num

    # SS未満の中間・修了テスト数
    @property
    def miss_test_num(self):
        return self.test_done_num - self.test_ss_num

    # 不受験の修了テスト数。受講が全て終わっているのに受けていなければ、1を返す
    @property
    def ignore_test_num(self):
        if (
            self.course_num == self.course_done_num
            and self.test_num > self.test_done_num
        ):
            return 1
        return 0

    # 完全修得か判定。受講修了, 確認テスト・修了テストが全てSS
    def is_perfect(self):
        return (
            self.course_num == self.course_done_num
            and self.test_num == self.test_ss_num
            and self.subtest_num == self.subtest_ss_num
        )

    # 補足欄に記述する文字列。TODO: インターフェースをPDFに寄せすぎ。
    @property
    def details(self) -> str:
        if self.course_num < 1 or self.subtest_num < 1:
            return ""

        res = []

        # 講座を全て受験し、中間・修了テストを全てSSで合格している場合
        if self.is_perfect():
            return "完全修得"

        # SS未満の確認テスト数が1以上の場合
        if self.miss_subtest_num > 0:
            res.append("確テSS未満アリ")

        # S未満の中間・修了テスト数が1以上の場合
        if self.miss_test_num > 0:
            res.append("修テSS未満アリ")

        # 確認テストを全て受験していない場合
        # 確認テスト数と講座数が一致しない場合があるので、その場合は割合で判定
        if (
            self.course_done_num / self.course_num
            > self.subtest_done_num / self.subtest_num
        ):
            res.append("確テ未受験アリ")

        # 講座を全て受験しているのに、中間・修了テストが残っている
        if self.ignore_test_num > 0:
            res.append("修テ未受験アリ")

        if len(res) == 0:
            return ""
        return ",".join(res)
