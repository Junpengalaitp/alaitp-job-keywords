import logging
import time
from collections import Counter
from multiprocessing import Manager, Process

from keywords.spacy_processing import generate_key_words_from_job_desc
from logger.logger import setup_logging
from post_processing.keyword_clean import standardize_keywords
from service.MongoService import get_all_jobs

setup_logging()
logger = logging.getLogger("fileLogger")


def process_job_description(job_description_list: list) -> dict:
    start = time.perf_counter()
    job_texts = [job['jobDescriptionText'] for job in job_description_list]
    keywords_list = []
    for text in job_texts:
        keywords_list.append(generate_key_words_from_job_desc(text))

    keywords_dict = add_result_to_dict(keywords_list)

    standardize_keywords(keywords_dict)

    sort_keywords_dict(keywords_dict)

    end = time.perf_counter()
    logger.info(f'Jobs keyword generation finished in {round(end - start, 4)} seconds,')
    return keywords_dict  # convert to json to keep the order during transaction


def process_jobs(source: str = 'all') -> dict:
    start = time.perf_counter()
    job_texts = get_all_jobs(source)
    end = time.perf_counter()
    logging.info(f'Retrieved {len(job_texts)} jobs from mongo: {source} in {round(end - start, 4)} seconds')

    # start = time.perf_counter()
    # Multiprocessing for signal job keywords
    keywords_list = Manager().list()
    jobs = [Process(target=get_job_keywords_list, args=(keywords_list, text)) for text in job_texts]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()

    keywords_dict = add_result_to_dict(keywords_list)
    logger.info(f'keywords_dict: {keywords_dict}')

    standardize_keywords(keywords_dict)

    sort_keywords_dict(keywords_dict)
    # end = time.perf_counter()
    # logger.info(f'Jobs keyword generation finished in {round(end - start, 4)} seconds,')
    return keywords_dict  # convert to json to keep the order during transaction


def get_job_keywords_list(keywords_list, job_text):
    keywords = generate_key_words_from_job_desc(job_text)
    keywords_list.append(keywords)


def add_result_to_dict(keywords_list: list) -> dict:
    keywords_dict = dict()
    for job_keywords in keywords_list:
        for standard_name in job_keywords:
            if standard_name not in keywords_dict:
                keywords_dict[standard_name] = job_keywords[standard_name]
            else:
                for keyword in job_keywords[standard_name]:
                    keywords_dict[standard_name].append(keyword)
    return keywords_dict


def sort_keywords_dict(keywords_dict: dict) -> None:
    # return top 20 keywords
    for standard_name in keywords_dict:
        keywords_dict[standard_name] = dict(Counter(keywords_dict[standard_name]).most_common(20))
