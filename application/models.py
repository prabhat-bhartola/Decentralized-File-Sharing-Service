from datetime import datetime
from application.database import db

class Files(db.Model):
    __tablename__ = 'files'
    file_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    file_size = db.Column(db.Float, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    uploaded_by = db.Column(db.String, default="anonymous")
    file_desc = db.Column(db.String, default="NULL")

    def __init__(self, file_name, file_type, file_size, file_path, uploaded_by, file_desc):
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.file_path = file_path
        self.uploaded_by = uploaded_by
        self.file_desc = file_desc
    
class Chats(db.Model):
    __tablename__ = 'chats'
    chat_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    written_by = db.Column(db.String, default="anonymous")
    datetime_created = db.Column(db.String)
    message = db.Column(db.String)

    def __init__(self, written_by, message):
        self.written_by = written_by
        self.message = message
        self.datetime_created = datetime.now()