from flask import Flask
from flask_restful import Api

from resources.keywords import Keywords

app = Flask(__name__)
api = Api(app)

api.add_resource(Keywords, "/keywords/<string:job_id>")


if __name__ == '__main__':
    app.run()
