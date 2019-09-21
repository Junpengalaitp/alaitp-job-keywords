from flask_restful import Resource, reqparse

from keywords.keyword_generator import process_jobs


class KeywordsMultiJobs(Resource):
    parser = reqparse.RequestParser()

    def get(self):
        job_keyword_dict = process_jobs()
        print(f"job keyword dict generated: {job_keyword_dict}")
        if job_keyword_dict:
            return job_keyword_dict
        
        return {"message": "Item not found"}, 404


