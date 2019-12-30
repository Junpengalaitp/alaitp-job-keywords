import logging
import time
from collections import Counter
from multiprocessing import Manager, Process
from typing import List, Dict

from keyword_processing.spacy_processing import generate_key_words_from_job_desc
from logger.logger import setup_logging
from post_processing.keyword_clean import get_standardized_keywords
from service.mongo_service import get_all_jobs

setup_logging()
logger = logging.getLogger("fileLogger")


def process_job_description(job_description_list: List[dict]) -> dict:
    start = time.perf_counter()
    keywords_list = []
    for job_description in job_description_list:
        job_keyword_dict = generate_key_words_from_job_desc(job_description['jobDescriptionText'])
        # job_description['keyword_processing'] = job_keyword_dict
        # keywords_list.append((job_description['jobId'], job_keyword))
        keywords_list.append(job_keyword_dict)

    keywords_dict = combine_result_to_dict(keywords_list)

    get_standardized_keywords(keywords_dict)

    sort_keywords_dict(keywords_dict)

    end = time.perf_counter()
    logger.info(f'Jobs keyword_processing generation finished in {round(end - start, 4)} seconds,')
    return keywords_dict  # convert to json to keep the order during transaction


def process_jobs(source: str = 'all') -> dict:
    start = time.perf_counter()
    job_texts = get_all_jobs(source)
    end = time.perf_counter()
    logging.info(f'Retrieved {len(job_texts)} jobs from mongo: {source} in {round(end - start, 4)} seconds')

    # start = time.perf_counter()
    # Multiprocessing for signal job keyword_processing
    # keywords_list = Manager().list()
    # jobs = [Process(target=get_job_keywords_list, args=(keywords_list, text)) for text in job_texts]
    # for job in jobs:
    #     job.start()
    # for job in jobs:
    #     job.join()
    keywords_list = []
    for text in job_texts:
        keywords_list.append(generate_key_words_from_job_desc(text))

    keywords_dict = combine_result_to_dict(keywords_list)
    logger.info(f'keywords_dict: {keywords_dict}')
    start = time.perf_counter()
    get_standardized_keywords(keywords_dict)
    end = time.perf_counter()
    logger.info(f'standardization finished in {round(end - start, 4)} seconds')
    sort_keywords_dict(keywords_dict)
    # end = time.perf_counter()
    # logger.info(f'Jobs keyword_processing generation finished in {round(end - start, 4)} seconds,')
    return keywords_dict  # convert to json to keep the order during transaction


# def get_job_keywords_list(keywords_list, job_text):
#     keyword_processing = generate_key_words_from_job_desc(job_text)
#     keywords_list.append(keyword_processing)


def combine_result_to_dict(keywords_list: List[dict]) -> Dict[str, list]:
    """
    Combine multiple job keyword dict result into one dict
    """
    keywords_dict = dict()
    for job_keywords in keywords_list:
        for label in job_keywords:
            if label not in keywords_dict:
                keywords_dict[label] = list(job_keywords[label].values())
            else:
                for keyword in job_keywords[label].values():
                    keywords_dict[label].append(keyword)
    return keywords_dict


def sort_keywords_dict(keywords_dict: dict) -> None:
    # return top 20 keyword_processing
    for standard_name in keywords_dict:
        keywords_dict[standard_name] = dict(Counter(keywords_dict[standard_name]).most_common(20))

