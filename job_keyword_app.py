from multiprocessing import Process

from random import randint

from flask import Flask
from waitress import serve



# flask server only for registering to eureka
from src.config.config_server import CONFIG
from src.config.eureka_config import connect_eureka
from src.message.consumer import start_messaging

app = Flask(__name__)


def start_app():
    SERVER_IP = CONFIG['web.server.ip']
    PORT = randint(27018, 65535)
    connect_eureka(SERVER_IP, PORT)
    serve(app, host=SERVER_IP, port=PORT)


def start_test_server():
    SERVER_IP = CONFIG['web.server.ip']
    PORT = 5000
    connect_eureka(SERVER_IP, PORT)
    # serve(app, host="localhost", port=PORT)
    app.run(host="0.0.0.0", port=PORT)


def start_web():
    start_test_server()


if __name__ == '__main__':
    web_process = Process(target=start_web)
    web_process.start()
    start_messaging()

