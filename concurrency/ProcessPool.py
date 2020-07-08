"""Handling jobs keyword generation. Each job has a process for keyword generation."""
import os
from concurrent.futures.process import ProcessPoolExecutor

import service.keyword_service

"""when job keyword are cached, the process won't use much cpu resources, so max_workers can be larger than cpu cores"""
max_workers = os.cpu_count() * 2

executor = ProcessPoolExecutor(max_workers=max_workers)


def insert_msg(job_map: dict):
    executor.submit(service.keyword_service.process_job_keywords(job_map))
