#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app\models\model_mysql.py

from . import db

class UserMysql(db.Model):
    __tablename__ = 'usermysql'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)