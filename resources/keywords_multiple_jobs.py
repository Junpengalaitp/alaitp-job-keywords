import logging

from flask_restful import Resource, reqparse

from keywords.keyword_generator import process_jobs
from keywords.spacy_processing import generate_key_words_from_job_desc


class KeywordsMultiJobs(Resource):
    parser = reqparse.RequestParser()

    def get(self, cache_id):
        print(f'received cache id : {cache_id}')
        job_keyword_dict = process_jobs(cache_id)
        print(f"job keyword dict generated: {job_keyword_dict}")
        if job_keyword_dict:
            return job_keyword_dict
        
        return {"message": "Item not found"}, 404


