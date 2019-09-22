import json
import logging
import time
from collections import Counter, OrderedDict
from multiprocessing import Manager, Process, current_process

from database.MongodbManager import MongoManager
from keywords.spacy_processing import generate_key_words_from_job_desc
from logger.logger import setup_logging

setup_logging()
logger = logging.getLogger("fileLogger")


standard_words = {
    'JavaScript': ['JS', 'Javascript', 'javascript'],
    'Python': ['python'],
    'Java': ['java', 'Java8', 'java8', 'Java11', 'java11'],
    'Node.js': ['NodeJs', 'NodeJS', 'node.js', 'Node.js', 'Node', 'node'],
    'HTML': ['HTML5'],
    'JSON': ['Json', 'json'],
    'jQuery': ['Jquery', 'JQuery'],
    'MongoDB': ['mongo', 'Mongo', 'MongoDb', 'mongodb', 'Mongo DB'],
    'Test-Driven Development': ['Test Driven Development', 'TDD'],
    'EcmaScript': ['ES2015', 'ES5', 'ES6', 'ES5/ES6', 'ES', 'ES7', 'EcmaScript', 'Ecmascript'],
    'MySQL': ['MySql',],
    'C': ['c'],
    'C++': ['c++', ],
    'TypeScript': ['Typescript'],
    'CSS': ['css', 'CSS3', 'css3', 'CSS4', 'css4'],
    'Erlang': ['erlang'],
    'Go': ['GO', 'go', 'Golang', 'GoLang'],
    'React': ['react', 'react.js'],
    'Ruby on Rails': ['Rails', 'rails'],

}


# def process_job(job_obj_id: str) -> dict:
#
#     job_desc_text = get_job_text_from_mongo(job_obj_id)
#
#     keywords_dict = generate_key_words_from_job_desc(job_desc_text)
#
#     return keywords_dict


def get_all_jobs() -> list:
    jobs_list = MongoManager().find_all()
    return [job['job_desc'] for job in jobs_list]


def process_jobs() -> dict:
    start = time.perf_counter()
    job_texts = get_all_jobs()
    end = time.perf_counter()
    logging.info(f'Job retrieving finished in {round(end - start, 4)} seconds')

    start = time.perf_counter()
    # Multiprocessing for signal job keywords
    keywords_list = Manager().list()
    jobs = [Process(target=get_job_keywords_list, args=(keywords_list, text)) for text in job_texts]
    for job in jobs:
        job.start()
    for job in jobs:
        job.join()

    # Add keywords to result dict
    keywords_dict = dict()
    for job_keywords in keywords_list:
        for standard_name in job_keywords:
            if standard_name not in keywords_dict:
                keywords_dict[standard_name] = job_keywords[standard_name]
            else:
                for keyword in job_keywords[standard_name]:
                    keywords_dict[standard_name].append(keyword)

    # Standardize keywords
    for value in keywords_dict.values():
        for index, keyword in enumerate(value):
            for standard_name, other_names in standard_words.items():
                if keyword in other_names or keyword.upper() in other_names or keyword.lower() in other_names:
                    value[index] = standard_name

    # Count and sort keywords
    for standard_name in keywords_dict:
        keywords_dict[standard_name] = OrderedDict(Counter(keywords_dict[standard_name]).most_common())

    end = time.perf_counter()
    logger.info(f'Jobs keyword generation finished in {round(end - start, 4)} seconds')
    return keywords_dict  # convert to json to keep the order during transaction


def get_job_keywords_list(keywords_list, job_text):
    keywords = generate_key_words_from_job_desc(job_text)
    keywords_list.append(keywords)

