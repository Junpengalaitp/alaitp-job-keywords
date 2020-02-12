import json
import logging
from random import randint

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from waitress import serve

from KeywordGenerator.KeywordGenerator import get_job_keyword_dict
from config.config_server import CONFIG
from config.eureka_config import connect_eureka

app = Flask(__name__)
CORS(app)
api = Api(app)


@app.route('/keywords', methods=['POST'])
def get_job_keywords():
    job_description_data = json.loads(request.data)
    logging.info(job_description_data)
    job_keyword_dict = get_job_keyword_dict(job_description_data)
    logging.info(f"job keyword_processing dict generated: {job_keyword_dict}")
    return job_keyword_dict


def start_app():
    SERVER_IP = CONFIG['web.server.ip']
    PORT = randint(27018, 65535)
    connect_eureka(SERVER_IP, PORT)
    serve(app, host=SERVER_IP, port=PORT)


if __name__ == '__main__':
    start_app()

