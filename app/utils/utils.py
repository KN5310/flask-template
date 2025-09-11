#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/utils/utils.py

from flask import url_for
import os

def cleaned_url(endpoint, **values):
    BASE_PATH = os.getenv("BASE_PATH", "").rstrip("/")
    ENV_TYPE = os.getenv("ENV_TYPE", "lolipop-test")

    url = url_for(endpoint, **values)

    url = url.replace("/index.cgi", "")

    if ENV_TYPE in ("lolipop-prod", "lolipop-test"):
        if not url.startswith(BASE_PATH):
            url = BASE_PATH + url
    elif ENV_TYPE == "docker":
        pass
    else:
        pass

    return url
