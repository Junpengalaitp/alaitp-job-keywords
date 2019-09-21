# import logging
#
# from flask_restful import Resource, reqparse
#
# from keywords.keyword_generator import process_job
# from keywords.spacy_processing import generate_key_words_from_job_desc
#
#
# class KeywordSingleJob(Resource):
#     parser = reqparse.RequestParser()
#
#     def get(self, job_id):
#         print(f'received job id : {job_id}')
#         job_keyword_dict = process_job(job_id)
#         print(f"job keyword dict generated: {job_keyword_dict}")
#         if job_keyword_dict:
#             return job_keyword_dict
#
#         return {"message": "Item not found"}, 404


