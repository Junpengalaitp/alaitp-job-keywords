import logging
import time
from typing import List

from keyword_processing.spacy_processing import generate_key_words_from_job_desc
from logger.logger import setup_logging

setup_logging()
logger = logging.getLogger("fileLogger")


def get_job_keyword_dict(job_description_list: List[dict]) -> dict:
    start = time.perf_counter()
    keyword_dict = {}
    for job_description in job_description_list:
        print(job_description)
        job_keyword = generate_key_words_from_job_desc(job_description['jobDescriptionText'])
        job_description['keyword'] = job_keyword
        print(job_description)
        keyword_dict[job_description['jobId']] = job_keyword
    end = time.perf_counter()
    logger.info(f'Jobs keyword_processing generation finished in {round(end - start, 4)} seconds,')
    return keyword_dict  # convert to json to keep the order during transaction
