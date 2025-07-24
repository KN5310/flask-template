#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/utils/utils.py

from flask import url_for
import os

# BASE_PATH定義（すでにある場合は重複注意）
BASE_PATH = os.getenv("BASE_PATH", "").rstrip("/")

# URL生成＋クリーン化
def cleaned_url(endpoint, **values):
    url = url_for(endpoint, **values)
    return BASE_PATH + url.replace('/index.cgi', '')