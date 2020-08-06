"""Handling jobs keyword generation. Each job has a process for keyword generation."""
import os
from concurrent.futures.process import ProcessPoolExecutor, BrokenProcessPool

from service.keyword_service import process_job_keywords

"""when job keyword are cached, the process won't use much cpu resources, so max_workers can be larger than cpu cores"""
max_workers = os.cpu_count() * 4


def init_executor():
    return ProcessPoolExecutor(max_workers=max_workers)


class ProcessPool:
    executor = init_executor()


def execute(r):
    try:
        ProcessPool.executor.submit(r)
    except BrokenProcessPool:
        ProcessPool.executor = ProcessPoolExecutor(max_workers=max_workers)
        ProcessPool.executor.submit(r)


def insert_msg(job_map: dict):
    execute(process_job_keywords(job_map))
