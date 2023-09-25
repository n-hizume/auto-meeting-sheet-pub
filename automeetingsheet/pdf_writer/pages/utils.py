import unicodedata
from PyPDF2 import PdfWriter


def get_best_font_size(max_size: float, max_width: int, text: str):
    """
    文字列と最大幅から、最適なフォントサイズを返す。
    文字列が短い時に大きくなり過ぎないようにmax_sizeも指定。
    小文字や半角文字は1マス分取らないので微調整している。
    TODO:
        もっといい方法がないかを検討。
        - reportlab.pdfbase.pdfmetrics.stringWidth() が最適に見えるがうまく動かなかった。
    """
    text_len = 0
    for c in text:
        res = unicodedata.east_asian_width(c)
        if res in "FWA":
            text_len += 1
        elif res in "HNa":
            text_len += 0.4
    if text_len == 0:
        text_len += 1
    return min(max_size, max_width / text_len)


# テストで使う用の、単一ページのPDFを作成する関数
def page_to_pdf(page, file_path):
    output = PdfWriter()
    output.add_page(page)
    with open(file_path, "wb") as f:
        output.write(f)
