import os

from concurrent.futures.process import ProcessPoolExecutor

import service.spacy_service

executor = ProcessPoolExecutor(max_workers=os.cpu_count())


def insert_msg(remotive_job):
    executor.submit(service.spacy_service.spacy_job_keyword(remotive_job.id, remotive_job.description_text))
