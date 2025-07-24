#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/routes/routes_main.py

from flask import Blueprint, render_template, current_app
from app.utils.utils import cleaned_url

routes_main = Blueprint("main", __name__)

@routes_main.route("/")
def index():
    current_app.logger.info("トップページにアクセスされました。")
    return render_template("index.html")
