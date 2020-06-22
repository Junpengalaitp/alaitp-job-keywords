import os

from concurrent.futures.process import ProcessPoolExecutor

import service.spacy_service

executor = ProcessPoolExecutor(max_workers=os.cpu_count())


def insert_msg(job_id: str, description: str, request_id: str):
    executor.submit(service.spacy_service.generate_job_keyword(job_id, description, request_id))
