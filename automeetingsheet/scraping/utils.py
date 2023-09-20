def strip(text: str):
    """
    不要な改行, 空白を削除する。
    HTML.textには両端以外にも改行が含まれていることがあるので、stripだけでは不十分
    """
    return text.replace("\n", "").strip()
