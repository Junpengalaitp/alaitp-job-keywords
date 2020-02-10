import json
import logging

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api
from py_eureka_client import eureka_client
from waitress import serve


# from resources.keywords_multiple_jobs import KeywordsMultiJobs
from KeywordGenerator.KeywordGenerator import get_job_keyword_dict
from config.read_config import get_config
from keyword_processing.keyword_generator import process_job_description
from resources.KeywordsMongo import KeywordsMongo

app = Flask(__name__)
CORS(app)
api = Api(app)


# api.add_resource(Keyword, "/keyword_processing")
api.add_resource(KeywordsMongo, "/keyword_processing/<string:source>")

SERVER_IP = get_config('WEB_SERVER', 'ip')
PORT = int(get_config('WEB_SERVER', 'port'))

# @app.route('/keywords', methods=['POST'])
# def get_keywords():
#     job_description_data = json.loads(request.data)
#     logging.info(job_description_data)
#     job_keyword_dict = process_job_description(job_description_data)
#     logging.info(f"job keyword_processing dict generated: {job_keyword_dict}")
#     return job_keyword_dict


@app.route('/keywords', methods=['POST'])
def get_job_keywords():
    job_description_data = json.loads(request.data)
    logging.info(job_description_data)
    job_keyword_dict = get_job_keyword_dict(job_description_data)
    logging.info(f"job keyword_processing dict generated: {job_keyword_dict}")
    return job_keyword_dict


def setEureka():
    eureka_client.init(eureka_server="http://localhost:8811/eureka",
                       app_name="job-keywords",
                       instance_host=SERVER_IP,
                       instance_port=PORT,
                       ha_strategy=eureka_client.HA_STRATEGY_RANDOM)


setEureka()

if __name__ == '__main__':
    serve(app, host=SERVER_IP, port=PORT)

