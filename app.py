import json
import logging

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_restful import Api

from keywords.keyword_generator import process_job_description
from resources.keywords_multiple_jobs import KeywordsMultiJobs

app = Flask(__name__)
CORS(app)
api = Api(app)

# api.add_resource(Keyword, "/keywords")
api.add_resource(KeywordsMultiJobs, "/keywords/<string:source>")


@app.route('/keywords', methods=['POST'])
def get_keywords():
    job_description_data = json.loads(request.data)
    job_keyword_dict = process_job_description(job_description_data)
    logging.info(f"job keyword dict generated: {job_keyword_dict}")
    return job_keyword_dict


if __name__ == '__main__':
    app.run(debug=False)
