import os

from concurrent.futures.process import ProcessPoolExecutor

import service.keyword_service

executor = ProcessPoolExecutor(max_workers=os.cpu_count())


def insert_msg(job_map: dict):
    executor.submit(service.keyword_service.publish_job_keywords(job_map))
