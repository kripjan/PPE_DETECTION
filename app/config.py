# config.py
import os

class Config:
    SECRET_KEY = 'krijan'
    SQLALCHEMY_DATABASE_URI = 'oracle+cx_oracle://ppe:ppe@KRICTUS:1521/XE'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # Add any other settings you want here
