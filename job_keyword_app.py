import json
from random import randint

from flask import Flask, request, jsonify
from waitress import serve

from service.job_keyword_service import get_job_keyword_dict
from config.config_server import CONFIG
from config.eureka_config import connect_eureka
from logger.logger import log

app = Flask(__name__)


@app.route('/keywords', methods=['POST'])
def get_job_keywords():
    job_description_data = json.loads(request.data)
    log.info(f"job_description_data: {request.data}")
    job_keyword_dict = get_job_keyword_dict(job_description_data)
    log.info(f"job keyword_processing dict generated: {job_keyword_dict}")
    return jsonify(job_keyword_dict)


def start_app():
    SERVER_IP = CONFIG['web.server.ip']
    PORT = randint(27018, 65535)
    connect_eureka(SERVER_IP, PORT)
    serve(app, host=SERVER_IP, port=PORT)


def start_test_server():
    SERVER_IP = CONFIG['web.server.ip']
    PORT = 5000
    connect_eureka(SERVER_IP, PORT)
    app.run(host="localhost", port=PORT)


if __name__ == '__main__':
    # start_app()
    start_test_server()


