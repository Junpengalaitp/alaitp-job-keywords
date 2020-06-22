from random import randint

from flask import Flask
from waitress import serve

from config.config_server import CONFIG
from config.eureka_config import connect_eureka

# flask server only for registering to eureka
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
    app.run(host="localhost", port=PORT)


