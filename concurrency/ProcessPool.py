import os

from concurrent.futures.process import ProcessPoolExecutor

from service.spacy_service import spacy_job_keyword

executor = ProcessPoolExecutor(max_workers=os.cpu_count())

def insert_msg(remotive_job):
    executor.submit(spacy_job_keyword(remotive_job.id, remotive_job.description_text))
