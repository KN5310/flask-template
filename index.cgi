#!/usr/bin/env python3
# index.cgi
# -------------------------------------------
# ロリポップなどCGI環境でFlaskアプリを動かすためのエントリポイントスクリプト
# WSGIアプリをCGI経由で起動し、.htaccessも自動生成します
# -------------------------------------------

import sys
import os
import stat

# WSGIアプリをCGI経由で起動するための標準ハンドラーをインポート
from wsgiref.handlers import CGIHandler

# Flaskアプリ作成関数をインポート（ファクトリパターン）
from app import create_app

# sys.pathに現在のスクリプトのディレクトリを先頭に追加
# これにより同じディレクトリ内のモジュールがimport可能になる
sys.path.insert(0, os.path.dirname(__file__))

# .envファイルから環境変数を読み込むためのモジュール
from dotenv import load_dotenv

# .envファイルのパスを決定（このスクリプトの 'key' フォルダ内）
dotenv_path = os.path.join(os.path.dirname(__file__), "key", ".env")

# .envファイルが存在すれば読み込む（環境変数を設定）
load_dotenv(dotenv_path=dotenv_path)

# 環境変数 BASE_PATH を取得（存在しなければ '/'）
# URLパスのベースを決めるために使う（後で .htaccessに利用）
base_path = os.getenv("BASE_PATH", "/").rstrip("/")

# .htaccessファイルのパス（このスクリプトのディレクトリ内）
htaccess_path = os.path.join(os.path.dirname(__file__), ".htaccess")

# もし .htaccess ファイルが存在しなければ自動生成する
if not os.path.exists(htaccess_path):
    # Apacheのmod_rewrite設定を作成
    htaccess_content = f"""RewriteEngine On
RewriteBase {base_path}/

RewriteCond %{{REQUEST_FILENAME}} !-f
RewriteCond %{{REQUEST_FILENAME}} !-d
RewriteRule ^(.*)$ index.cgi/$1 [QSA,L]
"""

    # ファイルを書き込み（ここをインデント）
    with open(htaccess_path, 'w') as f:
        f.write(htaccess_content)
        print(f".htaccess generated at {htaccess_path}")

# Flaskアプリケーションを作成（create_appはapp/__init__.py内の関数）
app = create_app()

# CGIHandlerでFlaskのWSGIアプリをCGIとして起動
CGIHandler().run(app)
