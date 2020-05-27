import os

from concurrent.futures.process import ProcessPoolExecutor

import service.spacy_service

executor = ProcessPoolExecutor(max_workers=os.cpu_count())


def insert_msg(job_id: str, description: str):
    executor.submit(service.spacy_service.spacy_job_keyword(job_id, description))
