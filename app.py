import json
import logging

from flask import Flask, request
from flask_cors import CORS
from flask_restful import Api

# from resources.keywords_multiple_jobs import KeywordsMultiJobs
from KeywordGenerator.KeywordGenerator import get_job_keyword_dict
from keyword_processing.keyword_generator import process_job_description
from resources.KeywordsMongo import KeywordsMongo

app = Flask(__name__)
CORS(app)
api = Api(app)

# api.add_resource(Keyword, "/keyword_processing")
api.add_resource(KeywordsMongo, "/keyword_processing/<string:source>")


@app.route('/keywords', methods=['POST'])
def get_keywords():
    job_description_data = json.loads(request.data)
    logging.info(job_description_data)
    job_keyword_dict = process_job_description(job_description_data)
    logging.info(f"job keyword_processing dict generated: {job_keyword_dict}")
    return job_keyword_dict


@app.route('/single-job-keywords', methods=['POST'])
def get_job_keywords():
    job_description_data = json.loads(request.data)
    logging.info(job_description_data)
    job_keyword_dict = get_job_keyword_dict(job_description_data)
    logging.info(f"job keyword_processing dict generated: {job_keyword_dict}")
    return job_keyword_dict


if __name__ == '__main__':
    app.run(debug=False)
