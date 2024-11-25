# config.py
import os

class DevConfig:
    SECRET_KEY = 'krijan'
    SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://ppe:ppe@KRICTUS:1521/XE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True

class EmptyDbConfig:
    SECRET_KEY = 'krijan'
    SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://ppe_empty:ppe_empty@KRICTUS:1521/XE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
