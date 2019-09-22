import logging

from flask_restful import Resource, reqparse

from keywords.keyword_generator import process_jobs
from logger.logger import setup_logging

setup_logging()
logger = logging.getLogger("fileLogger")


class KeywordsMultiJobs(Resource):
    parser = reqparse.RequestParser()

    def get(self, source: str = None) -> dict:
        job_keyword_dict = process_jobs(source)
        logging.info(f"job keyword dict generated: {job_keyword_dict}")
        if job_keyword_dict:
            return job_keyword_dict
        
        return {"message": "Item not found"}, 404


