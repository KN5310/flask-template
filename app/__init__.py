#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/__init__.py

from flask import Flask, url_for
from flask_wtf import CSRFProtect
import os, traceback
import logging
from dotenv import load_dotenv

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from app.models.model_mysql import db, UserMysql  
from app.utils.utils import cleaned_url  

migrate = Migrate()
csrf = CSRFProtect()

dotenv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "key", ".env"))
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
else:
    print(f"[Warning] .env file not found at {dotenv_path}")

log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
os.makedirs(log_dir, exist_ok=True)
log_path = os.path.join(log_dir, "app.log")
logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s in %(module)s: %(message)s",
    handlers=[logging.FileHandler(log_path, encoding="utf-8")],
)

def create_app():
    try:
        app = Flask(
            __name__,
            template_folder="../templates",
            static_folder="../static"
        )
        app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default-unsafe-key")

        ENV_TYPE = os.getenv("ENV_TYPE", "lolipop-test")
        if ENV_TYPE == "docker":
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_DOCKER")
        elif ENV_TYPE == "lolipop-test":
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_LOLIPOP_TEST")
        elif ENV_TYPE == "lolipop-prod":
            app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI_LOLIPOP_PROD")
        else:
            raise ValueError(f"Unknown ENV_TYPE: {ENV_TYPE}")

        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        csrf.init_app(app)
        db.init_app(app)
        migrate.init_app(app, db)

        from app.routes.routes_main import routes_main
        app.register_blueprint(routes_main)

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
            f"Loaded ENV_TYPE: {ENV_TYPE}, BASE_PATH: {os.getenv('BASE_PATH')}, SITE_ROOT_URL: {os.getenv('SITE_ROOT_URL')}"
        )

        return app

    except Exception as e:
        error_message = f"[Startup Error] {e}\n{traceback.format_exc()}"
        print(error_message)
        logging.exception(error_message)
        raise
