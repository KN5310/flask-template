#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/__init__.py

from flask import Flask, url_for
from flask_wtf import CSRFProtect
import os, traceback, logging
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.models.model_mysql import db, UserMysql
from app.models.model_sqlite import db_sqlite, UserSqlite
from app.utils.utils import cleaned_url

migrate = Migrate()
csrf = CSRFProtect()

# dotenv読み込み
dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "key", ".env"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"[Warning] .env file not found at {dotenv_path}")

# ログ設定
log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[logging.FileHandler(log_path, encoding="utf-8")],
)

# SQLite DBファイル作成
data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
os.makedirs(data_dir, exist_ok=True)
sqlite_db_path = os.path.join(data_dir, "sqlite.db")
if not os.path.exists(sqlite_db_path):
    import sqlite3
    try:
        conn = sqlite3.connect(sqlite_db_path)
        conn.close()
        print(f"[Info] SQLite DB を作成しました: {sqlite_db_path}")
    except Exception as e:
        print(f"[Error] SQLite DB の作成に失敗しました: {e}")

def create_app():
    try:
        app = Flask(
            __name__,
            template_folder="../templates",
            static_folder="../static"
        )
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-unsafe-key")
        ENV_TYPE = os.getenv("ENV_TYPE", "lolipop-test")
        ENV_DB = os.getenv("ENV_DB", "sqlite")  # 'mysql' or 'sqlite'

        # データベース設定
        if ENV_DB == "mysql":
            if ENV_TYPE == "docker":
                app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_DOCKER")
            elif ENV_TYPE == "lolipop-test":
                app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_LOLIPOP_TEST")
            elif ENV_TYPE == "lolipop-prod":
                app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_LOLIPOP_PROD")
            else:
                raise ValueError(f"Unknown ENV_TYPE: {ENV_TYPE}")
        elif ENV_DB == "sqlite":
            app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{sqlite_db_path}"
        else:
            raise ValueError(f"Unknown ENV_DB: {ENV_DB}")

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        # CSRF
        csrf.init_app(app)

        # DB初期化
        if ENV_DB == "mysql":
            db.init_app(app)
            migrate.init_app(app, db)
        elif ENV_DB == "sqlite":
            # SQLite は init_app を先に呼ぶ
            db_sqlite.init_app(app)

            # app_context 内でテーブル作成
            with app.app_context():
                db_sqlite.create_all()

        # -----------------------------
        # DBテーブル作成/初期化（Docker MySQL 用）
        from sqlalchemy import text
        with app.app_context():
            if ENV_DB == "mysql" and ENV_TYPE == "docker":
                try:
                    with db.engine.connect() as conn:
                        result = conn.execute(text("SHOW TABLES;"))
                        for row in result.fetchall():
                            table = row[0]
                            if table != "alembic_version":
                                conn.execute(text(f"DROP TABLE `{table}`;"))
                                app.logger.info(f"Docker環境: テーブル {table} を削除しました")
                    db.create_all()
                    app.logger.info("Docker環境: MySQLモデル通りにテーブルを作成しました")
                except Exception as e:
                    app.logger.error(f"MySQLテーブル作成/削除エラー: {e}")
        # -----------------------------

        # ルート登録
        from app.routes.routes_main import routes_main
        app.register_blueprint(routes_main)

        # ユーティリティ関数
        def static_url(filename):
            url = url_for("static", filename=filename)
            return url.replace("/index.cgi", "")

        @app.context_processor
        def utility_processor():
            return dict(
                static_url=static_url,
                cleaned_url=cleaned_url,
                site_name="flask-templateページ",
                base_path=os.getenv("BASE_PATH", "").rstrip("/"),
                site_root_url=os.getenv("SITE_ROOT_URL", "").rstrip("/"),
            )

        app.logger.info(
            f"Loaded ENV_TYPE: {ENV_TYPE}, ENV_DB: {ENV_DB}, BASE_PATH: {os.getenv('BASE_PATH')}, SITE_ROOT_URL: {os.getenv('SITE_ROOT_URL')}"
        )

        return app

    except Exception as e:
        error_message = f"[Startup Error] {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.exception(error_message)
        raise
