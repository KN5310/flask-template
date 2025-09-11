#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app\models\model_test.py

from . import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)