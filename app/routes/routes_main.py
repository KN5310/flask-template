#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/routes/routes_main.py

import os
import smtplib
from email.mime.text import MIMEText
from flask import Blueprint, render_template, current_app, request, redirect, flash
from app.utils.utils import cleaned_url
from app.models import db, User

routes_main = Blueprint("main", __name__)


@routes_main.route("/")
def index():
    current_app.logger.info("トップページにアクセスされました。")
    return render_template("index.html")


@routes_main.route("/test")
def test_page():
    current_app.logger.info("テストページにアクセスされました。")

    users = User.query.all()

    return render_template("test.html", users=users)


@routes_main.route("/register_name", methods=["POST"])
def register_name():
    username = request.form.get("username", "").strip()
    if username:

        new_user = User(name=username)
        db.session.add(new_user)
        db.session.commit()
        flash(f"{username} を登録しました！", "success")
    else:
        flash("名前を入力してください", "error")
    return redirect(cleaned_url("main.test_page"))


@routes_main.route("/delete_all_users", methods=["POST"])
def delete_all_users():
    try:
        num_deleted = User.query.delete()
        db.session.commit()
        flash(f"{num_deleted} 件のユーザーを削除しました！", "success")
    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"ユーザー全削除エラー: {e}")
        flash("ユーザー全削除に失敗しました。", "error")
    return redirect(cleaned_url("main.test_page"))


@routes_main.route("/send_email", methods=["POST"])
def send_email():
    subject = request.form.get("subject", "").strip()
    body = request.form.get("body", "").strip()

    if not subject or not body:
        flash("件名と本文を入力してください", "error")
        return redirect(cleaned_url("main.test_page"))

    SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.lolipop.jp")
    SMTP_PORT = int(os.environ.get("SMTP_PORT", 465))
    EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS", "test@hyogokurumi.com")
    EMAIL_PASS = os.environ.get("EMAIL_PASS")

    try:
        msg = MIMEText(body, "plain", "utf-8")
        msg["Subject"] = subject
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = EMAIL_ADDRESS

        with smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT) as server:
            server.login(EMAIL_ADDRESS, EMAIL_PASS)
            server.send_message(msg)

        flash("メールを送信しました！", "success")
    except Exception as e:
        current_app.logger.error(f"メール送信エラー: {e}")
        flash("メール送信に失敗しました。", "error")

    return redirect(cleaned_url("main.test_page"))