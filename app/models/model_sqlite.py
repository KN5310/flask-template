#!/usr/local/bin/python3.7
# -*- coding: utf-8 -*-
# app/models/model_sqlite.py

from flask_sqlalchemy import SQLAlchemy

# SQLite専用のSQLAlchemyインスタンス
db_sqlite = SQLAlchemy()

class UserSqlite(db_sqlite.Model):
    __tablename__ = "users_sqlite"
    id = db_sqlite.Column(db_sqlite.Integer, primary_key=True)
    name = db_sqlite.Column(db_sqlite.String(255), nullable=False)