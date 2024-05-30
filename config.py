import os

class Config:
    SECRET_KEY = os.urandom(24)
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://username:password@localhost/db_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
