import os


class Config:
    SECRET_KEY = os.urandom(24)
    UPLOAD_FOLDER = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'uploads')
    DB_HOST = "127.0.0.2"
    DB_USER = "root"
    DB_PASSWORD = "root@1234"
    DB_NAME = "data_visualizer"
