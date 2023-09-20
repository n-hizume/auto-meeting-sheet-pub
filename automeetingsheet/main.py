# TODO: import長いのどうにかしたい。特にGUI
from datetime import date
from automeetingsheet.config.env_config import EnvConfig
from automeetingsheet.config.login_config import LoginConfig
from automeetingsheet.models.student_info import StudentInfo
from automeetingsheet.logger.logger import Logger
from automeetingsheet.database.student_info_handler import StudentInfoHandler
from automeetingsheet.gui.login import LoginGUI
from automeetingsheet.gui.error import ErrorGUI
from automeetingsheet.gui.gui_base import EventKey
from automeetingsheet.gui.select_school import SelectSchoolGUI
from automeetingsheet.gui.select_students import SelectStudentsGUI
from automeetingsheet.gui.select_group import SelectGroupGUI
from automeetingsheet.gui.select_continue import SelectContinueGUI
from automeetingsheet.pdf_writer.pdf_writer import PDFWriter
from automeetingsheet.scraping.session import WebSession

TODAY = date.today()


def main():
    # 毎月１日に古いデータを消す
    if TODAY.day == 1:
        StudentInfoHandler.delete_old_records(days=100)
        print("Deleted old records")

    login_config = set_login_config()
    if login_config is None:
        raise ValueError("LoginGUI is closed.")

    env_config = EnvConfig.read()

    # Webページにログイン
    session = WebSession(proxy=env_config.proxy)
    try:
        session.login(login_config.id, login_config.password)
    except Exception as e:
        ErrorGUI.show(title="ログインに失敗しました。ID・パスワードをお確かめください。", text=str(e))
        return

    # 校舎の選択
    schools = session.get_school_list()
    if login_config.school not in schools:
        # 存在しない校舎名だった場合、選択してもらいconfigを上書き
        school = SelectSchoolGUI.show(
            invalid_school=login_config.school, school_list=schools
        )
        login_config.school = school
        login_config.write()

    session.select_school(login_config.school)

    # 今曜日のグループの情報をまず取得する
    groups = session.get_group_list()
    weekday_groups = extract_weekday_groups(groups)
    group_dict = dict([])
    for group_name in weekday_groups:
        group_dict[group_name] = session.get_student_info_list(group_name)

    # 今曜日のグループの全情報をDBに格納する
    for group_name in group_dict.keys():
        StudentInfoHandler.insert_records(group_dict[group_name])
    print("Today's group info is registered to database.")

    printed_students: list[StudentInfo] = []

    # 今曜日のグループから、印刷する生徒を選択
    selected = SelectStudentsGUI.show(group_dict, default=True)
    selected_students = extract_selected_student(group_dict, selected)
    for student in selected_students:
        printed_students.append(student)
        print(f"Add: {student.name}")

    # 終了されるまで、残りのグループから印刷する生徒を選択
    while True:
        is_continue = SelectContinueGUI.show()
        if not is_continue:
            break

        res, selected_group = SelectGroupGUI.show(groups)
        # グループ全員を印刷
        if res == EventKey.ALL:
            selected_students = session.get_student_info_list(selected_group)
        # 一部の生徒を印刷
        elif res == EventKey.SOME:
            students = session.get_student_info_list(selected_group)
            selected = SelectStudentsGUI.show({selected_group: students})
            selected_students = extract_selected_student(
                {selected_group: students}, selected
            )
        # 終了などが押された場合
        else:
            break

        for student in selected_students:
            printed_students.append(student)
            print(f"Add: {student.name}")

    # 印刷する生徒たちの詳細情報を取得
    session.add_students_detail(printed_students)

    pdf_writer = PDFWriter(login_config)
    for student in printed_students:
        past_records = StudentInfoHandler.get_records(student.name, num=6)

        # 過去の学習履歴をDBから取得。一番上が今日の日付なら削除して最新５つ
        if len(past_records) > 0:
            past_records = (
                past_records[1:]
                if past_records[0].created_date == TODAY
                else past_records[:5]
            )

        pdf_writer.add_student(student, past_records)

    pdf_writer.save(f"output/generate.pdf")


def set_login_config() -> LoginConfig | None:
    """
    エラー(日付の表記ミスなど)が起きたら、もう一度やり直すように促す。
    ログイン画面で終了ボタンが押された, もしくはエラーでやり直さなかった時にはNoneを返す
    """
    while True:
        try:
            return LoginGUI.show()
        except Exception as e:
            res = ErrorGUI.show(title="無効な値です", text=str(e), enable_again=True)
            if res != EventKey.AGAIN:
                return None


def extract_weekday_groups(groups: list[str]) -> list[str]:
    """
    今週のグループのみを抽出する
    """
    weekdays_str = ["月", "火", "水", "木", "金", "土", "日"]
    weekday_str = weekdays_str[TODAY.weekday()]
    return [group for group in groups if f"{weekday_str}曜" in group]


def extract_selected_student(
    group_dict: dict[str, list[StudentInfo]], selected: list[bool]
) -> list[StudentInfo]:
    """
    選択された生徒を抽出する
    """
    if len(selected) == 0:
        return []
    student_list = []
    for group_name in group_dict.keys():
        student_list.extend(group_dict[group_name])

    return [student_list[i] for i in range(len(student_list)) if selected[i]]


if __name__ == "__main__":
    logger = Logger(__name__)
    try:
        main()
    except Exception as e:
        # エラーが起きた場合、ログファイルに出力+エラーのGUIを表示
        logger.error()
        ErrorGUI.show_by_error(e)
