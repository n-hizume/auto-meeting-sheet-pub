# AutoMeetingSheet

## 実行方法
```
python automeetingsheet/main.py
```

もしくはWindowsの場合、`autoMeetingSheet.bat`を実行



## テスト
```
python -m unittest
```


`pdf_writer, gui, scraping/session` に関しては各クラス定義ファイルを実行することで挙動確認

## 各フォルダ説明
- automeetingsheet
  - config : /config/*.json に対応する構造定義と操作のモジュール
  - database : DBの定義・操作のモジュール
  - gui : ユーザに表示するGUIのモジュール
  - logger : ログ管理モジュール
  - models : 生徒情報・講座情報などのインターフェース定義
  - pdf_writer : PDF作成のためのモジュール
    - pages : PDFに使うページの管理
  - scraping : Webからデータを取得するモジュール. ※実装の大半は企業秘密
  - main.py : 実行スクリプト
- config : `automeetingsheet/config`に対応するjsonファイル
- database : `automeetingsheet/database`に対応するDBファイルの置き場
- docs : 操作マニュアルやソフトウェア仕様書などの管理
- logs : `automeetingsheet/logger`に対応するlogファイルの置き場
- output : 作成されるPDFの置き場
- templates : `automeetingsheet/pdf_writer/pages`に対応するPDFページテンプレ
- tests : `automeetingsheet/`と同じ構造を持つテスト用フォルダ
- autoMeetingSheet.bat : Windows環境で使える実行スクリプト
- requirements.txt : Pythonのライブラリ管理
