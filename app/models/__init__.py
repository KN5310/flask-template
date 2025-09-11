#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/models/__init__.py

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .model_test import *