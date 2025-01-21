# config.py
import os


class DevConfig:
    SECRET_KEY = "krijan"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://ppe:ppe@localhost:5432/ppe"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True


class EmptyDbConfig:
    SECRET_KEY = "krijan"
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://ppe:ppe@localhost:5432/ppe_empty"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
