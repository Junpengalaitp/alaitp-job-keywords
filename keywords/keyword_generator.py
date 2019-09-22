import logging
import time
from collections import Counter, OrderedDict
from multiprocessing import Manager, Process

from database.MongodbManager import MongoManager
from keywords.spacy_processing import generate_key_words_from_job_desc
from logger.logger import setup_logging
from static.constants import standard_words

setup_logging()
logger = logging.getLogger("fileLogger")


def get_all_jobs(source: str = 'all') -> list:
    if source == 'all':
        jobs_list = MongoManager().find_all()
    else:
        jobs_list = MongoManager().find_by_source(source)

    return [job['job_desc'] for job in jobs_list]


def process_jobs(source: str = 'all') -> dict:
    start = time.perf_counter()
    job_texts = get_all_jobs(source)
    end = time.perf_counter()
    logging.info(f'Retrieved {len(job_texts)} jobs from mongo: {source} in {round(end - start, 4)} seconds')

    start = time.perf_counter()
    # Multiprocessing for signal job keywords
    keywords_list = Manager().list()
    jobs = [Process(target=get_job_keywords_list, args=(keywords_list, text)) for text in job_texts]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()

    keywords_dict = add_result_to_dict(keywords_list)

    standardize_keywords(keywords_dict)

    sort_keywords_dict(keywords_dict)

    end = time.perf_counter()
    logger.info(f'Jobs keyword generation finished in {round(end - start, 4)} seconds,')
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


def standardize_keywords(keywords_dict: dict) -> None:
    for value in keywords_dict.values():
        for index, keyword in enumerate(value):
            for standard_name, other_names in standard_words.items():
                if keyword in other_names or keyword.upper() in other_names or keyword.lower() in other_names:
                    value[index] = standard_name


def sort_keywords_dict(keywords_dict: dict) -> None:
    # Count and sort keywords
    for standard_name in keywords_dict:
        keywords_dict[standard_name] = OrderedDict(Counter(keywords_dict[standard_name]).most_common())
