import os
from flask import Flask
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db

from flask_socketio import SocketIO, send


app = None

def create_app():
    app = Flask(__name__, template_folder="templates")

    socketio = SocketIO(app)
    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting local Development")
        app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    return app, socketio

app, socketio = create_app()

config.socketio = socketio
# print(config.socketio)

@socketio.on('message')
def handle_message(msg):
    print('Message: ', msg)
    send(msg, broadcast=True)

from application.controllers import *

if __name__ == '__main__':
    # app.run(
    #     host='192.168.29.83',
    #     port=8080
    # )

    socketio.run(app,
        host='192.168.29.83',
        port=8080
    )