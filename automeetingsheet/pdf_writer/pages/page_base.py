from abc import ABCMeta, abstractmethod
import io
import os
from PyPDF2 import PageObject, PdfReader, PdfWriter
from reportlab.lib.pagesizes import A4, landscape
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.cidfonts import UnicodeCIDFont

TEMPLATE_DIR = "templates"

FONT_NAME = "HeiseiMin-W3"
pdfmetrics.registerFont(UnicodeCIDFont(FONT_NAME))


# Pageの基底クラス
class PageBase(PageObject, metaclass=ABCMeta):
    template_file_name: str = ""

    @classmethod
    @property
    def template_file_path(cls) -> str:
        """
        テンプレートのパスを返す。ファイル名は個々の継承先で設定
        """
        if cls.template_file_name == "":
            raise NotImplementedError("cls.template_file_nameが設定されていません。")
        return f"{TEMPLATE_DIR}/{cls.template_file_name}"

    @classmethod
    @abstractmethod
    def create(cls) -> "PageBase":
        """
        Override対象。この関数を呼び出すことで、テンプレートを元にページを作成する。
        TODO:
            initで作るべきか要検討
            内部状態を持たず完成品を渡すイメージなので、createの方が明確な気もする
        """
        raise NotImplementedError("create関数が実装されていません。")

    @classmethod
    def create_graph_paper(cls) -> "PageBase":
        """
        座標特定のために、テンプレートに座標情報を書き込む。
        """
        page = PdfReader(cls.template_file_path).pages[0]

        # A4は絶対。縦か横かだけをtemplateから推定
        w, h = page.mediabox.width, page.mediabox.height
        sizes = landscape(A4) if w > h else A4

        packet = io.BytesIO()
        can = canvas.Canvas(packet, pagesize=sizes)
        can.setFontSize(1)

        # 座標の書き込み
        for x in range(0, int(w), 10):
            for y in range(0, int(h), 10):
                can.drawString(x, y, f"<-({x},{y})")

        can.save()
        new_page = cls.merge(packet, page)

        output = PdfWriter()
        output.add_page(new_page)

        if not os.path.exists(f"{TEMPLATE_DIR}/graph"):
            os.mkdir(f"{TEMPLATE_DIR}/graph")
        with open(f"{TEMPLATE_DIR}/graph/{cls.template_file_name}", "wb") as f:
            output.write(f)

    @staticmethod
    def merge(packet, base_page: PageObject) -> PageObject:
        """
        各継承先で使用する、テンプレートとのマージ処理
        TODO: こういうのを継承としてやるべきなのか、別のクラスに役割を担わせるべきなのか検討
        """
        packet.seek(0)
        new_page = PdfReader(packet).pages[0]
        base_page.merge_page(new_page)
        return base_page
