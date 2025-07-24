#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/__init__.py

"""
Flaskアプリケーションファクトリー

このファイルは Flask の Application Factory パターンに従い、
create_app() 関数によってアプリインスタンスを生成します。

主な役割:
- .env ファイルから環境変数を読み込み（SECRET_KEY, BASE_PATH など）
- Flask アプリインスタンスを生成し設定を適用
- CSRF 保護（Flask-WTF）の適用
- Blueprint（ルーティング）の登録
- ログファイル（logs/app.log）へのログ出力設定
- 静的ファイルのURL整形用関数 static_url の定義
- テンプレート内で利用できるグローバル変数・関数の登録
- アプリ内の全例外をログ出力＋共通エラーページで表示

補足:
- 初期化処理内でのエラー発生をテストできるよう、
  create_app() 内に「わざとエラーを発生させる」処理が
  コメントアウトで仕込んであります。

この構成により、ロリポップのような CGI サーバー環境でも、
Flask アプリを柔軟に初期化・運用できるように設計されています。
"""

from flask import Flask, url_for
from flask_wtf import CSRFProtect
import os
import traceback
from app.utils.utils import cleaned_url

import logging
from dotenv import load_dotenv

# .env 読み込み
dotenv_path = os.path.join(os.path.dirname(__file__), "..", "key", ".env")
load_dotenv(dotenv_path)

# ログ設定（create_appの外で先に設定）
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[logging.FileHandler(log_path, encoding="utf-8")],
)

csrf = CSRFProtect()  # CSRFProtectのインスタンス作成

def create_app():

    try:
        app = Flask(__name__, template_folder="../templates")

        # # ここでわざとエラーを発生させる（例: RuntimeError）
        # raise RuntimeError("テスト用の初期化エラー発生")

        # SECRET_KEYはCSRFに必須なので必ず設定する
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-unsafe-key")

        # CSRFProtectをFlaskアプリに登録
        csrf.init_app(app)

        from app.routes.routes_main import routes_main

        app.register_blueprint(routes_main)

        # 静的ファイルURLのindex.cgi除去版をローカル関数で定義
        def static_url(filename):
            url = url_for("static", filename=filename)
            return url.replace("/index.cgi", "")

        app.logger.info(
            f"Loaded BASE_PATH: {os.getenv('BASE_PATH')}, SITE_ROOT_URL: {os.getenv('SITE_ROOT_URL')}",
        )

        # テンプレートで使える関数群を登録
        @app.context_processor
        def utility_processor():
            return dict(
                static_url=static_url,
                cleaned_url=cleaned_url,
                site_name="flask-templateページ",
                base_path=os.getenv("BASE_PATH", "").rstrip("/"),
                site_root_url=os.getenv("SITE_ROOT_URL", "").rstrip("/"),
            )

        return app

    except Exception as e:
        # 起動時の初期化エラーを標準出力に表示＋ログにも残す
        error_message = f"[Startup Error] {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.exception(error_message)
        raise  # 再送出してアプリケーションを止める
