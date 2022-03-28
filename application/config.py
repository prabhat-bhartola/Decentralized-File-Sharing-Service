import os
# PRINTS THE PATH OF THE FOLDER OF CURRENT FILE
basedir = os.path.abspath(os.path.dirname(__file__))
socketio = None

class Config():
    DEBUG = False   #PRINTS DEBUG INFORMATION
    SQLITE_DB_DIR = None    #SQLITE DATABASE PATH
    SQLALCHEMY_DATABASE_URI = None
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class LocalDevelopmentConfig(Config):
    SQLITE_DB_DIR = os.path.join(basedir, "../db_directory")
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(SQLITE_DB_DIR, "prod_db.sqlite3")
    CLIENT_FILES = os.path.join(basedir, "../static/client/file")
    DEBUG = True
