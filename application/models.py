from datetime import date, datetime
from application.database import db

class Users(db.Model):
    __tablename__ = 'users'
    ip_addr = db.Column(db.String, primary_key=True)
    user_name = db.Column(db.String, default="anonymous")
    conn_status = db.Column(db.Integer, default=1)
    host_sdp = db.Column(db.String, unique=True)
    client_sdp = db.Column(db.String)
    socket_id = db.Column(db.String)

    def __init__(self, ip_address, user_name, client_sdp):
        self.ip_addr = ip_address
        self.user_name = user_name
        self.client_sdp = client_sdp


class Files(db.Model):
    __tablename__ = 'files'
    file_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    file_name = db.Column(db.String, nullable=False)
    file_type = db.Column(db.String, nullable=False)
    file_size = db.Column(db.String, nullable=False)
    file_path = db.Column(db.String, nullable=False)
    file_desc = db.Column(db.String, default="NULL")
    u_ip = db.Column(db.String, db.ForeignKey('users.ip_addr'), nullable=False, default="127.0.0.1")

    def __init__(self, file_name, file_type, file_size, file_path, file_desc, u_ip):
        self.file_name = file_name
        self.file_type = file_type
        self.file_size = file_size
        self.file_path = file_path
        self.file_desc = file_desc
        self.u_ip = u_ip


class Chats(db.Model):
    __tablename__ = 'chats'
    chat_no = db.Column(db.Integer, autoincrement=True, primary_key=True)
    date_created = db.Column(db.String)
    time_created = db.Column(db.String)
    content = db.Column(db.String)
    author_ip = db.Column(db.String, db.ForeignKey('users.ip_addr'))

    def __init__(self, message, author_ip):

        self.date_created = str(date.today().strftime('%d-%m-%Y'))
        self.time_created = datetime.strptime(str(datetime.now().time())[:5], "%H:%M").strftime("%I:%M %p")
        self.content = message
        self.author_ip = author_ip