from flask import Flask
from flask_restful import Api

from resources.keywords_multiple_jobs import KeywordsMultiJobs

app = Flask(__name__)
api = Api(app)

# api.add_resource(KeywordSingleJob, "/keywords/<string:job_id>")
api.add_resource(KeywordsMultiJobs, "/keywords-all")

if __name__ == '__main__':
    app.run(debug=False)
