import logging

from flask_restful import Resource, reqparse

from keywords.keyword_generator import generate_key_words_from_job_desc


class Keywords(Resource):
    parser = reqparse.RequestParser()

    def get(self, job_id):
        logging.info(f'received job id : {job_id}')
        job_keyword_dict = generate_key_words_from_job_desc('5d7cc22689005551ffa80114')
        logging.info(job_keyword_dict)
        if job_keyword_dict:
            return job_keyword_dict
        
        return {"message": "Item not found"}, 404


