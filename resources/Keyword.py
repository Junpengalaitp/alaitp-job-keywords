import logging

from flask_restful import Resource

from logger.logger import setup_logging

setup_logging()
logger = logging.getLogger("fileLogger")


class Keyword(Resource):

    def post(self):
        pass


