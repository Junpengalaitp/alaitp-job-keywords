import logging
import time
from typing import List

from keyword_processing.keyword_generator import combine_result_to_dict, sort_keywords_dict
from keyword_processing.spacy_processing import generate_key_words_from_job_desc
from logger.logger import setup_logging
from post_processing.keyword_clean import get_standardized_keywords

setup_logging()
logger = logging.getLogger("fileLogger")


def get_job_keyword_dict(job_description_list: List[dict]) -> dict:
    start = time.perf_counter()
    keyword_dict = {'keywordByJob': {}, 'keywordByLabel': {}}
    for job_description in job_description_list:
        job_keywords = generate_key_words_from_job_desc(job_description['jobDescriptionText'])
        job_description['keyword'] = job_keywords
        keyword_dict['keywordByJob'][job_description['jobId']] = job_keywords
        for label in job_keywords:
            if label not in keyword_dict['keywordByLabel']:
                keyword_dict['keywordByLabel'][label] = list(job_keywords[label].values())
            else:
                for keyword in job_keywords[label].values():
                    keyword_dict['keywordByLabel'][label].append(keyword)

    keyword_dict['keywordByLabel'] = get_standardized_keywords(keyword_dict['keywordByLabel'])

    sort_keywords_dict(keyword_dict['keywordByLabel'])
    logger.info(keyword_dict)
    end = time.perf_counter()
    logger.info(f'Jobs keyword_processing generation finished in {round(end - start, 4)} seconds,')
    return keyword_dict  # convert to json to keep the order during transaction

