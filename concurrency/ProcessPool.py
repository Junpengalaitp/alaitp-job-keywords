import os

from concurrent.futures.process import ProcessPoolExecutor

import service.spacy_service

executor = ProcessPoolExecutor(max_workers=os.cpu_count())


def insert_msg(job_map: dict):
    executor.submit(service.spacy_service.get_keywords_publish(job_map))
