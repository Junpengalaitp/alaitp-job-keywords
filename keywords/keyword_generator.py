import concurrent
import json
import time
from collections import Counter, OrderedDict
from multiprocessing import Manager, Process, cpu_count, Pool, current_process

from database.MongodbManager import MongoManager
from keywords.spacy_processing import generate_key_words_from_job_desc

standard_words = {
    'JavaScript': ['JS', 'Javascript', 'javascript'],
    'Python': ['python'],
    'Node.js': ['NodeJs', 'NodeJS', 'node.js', 'Node.js', 'Node', 'node'],
    'HTML': ['HTML5'],
    'JSON': ['Json', 'json'],
    'jQuery': ['Jquery', 'JQuery'],
    'MongoDB': ['mongo', 'Mongo', 'MongoDb', 'mongodb', 'Mongo DB'],
    'Test-Driven Development': ['Test Driven Development', 'TDD'],
    'ES5/ES6': ['ES2015', 'ES5', 'ES6', 'ES5/ES6'],
    'MySQL': ['MySql',]
}


def process_job(job_obj_id: str) -> dict:

    job_desc_text = get_job_text_from_mongo(job_obj_id)

    keywords_dict = generate_key_words_from_job_desc(job_desc_text)

    return keywords_dict


def get_job_text_from_mongo(job_obj_id: str) -> str:
    job = MongoManager().find_one_by_obj_id(job_obj_id)
    job_desc_text = job['job_desc']
    return job_desc_text


def start_process():
    print('Starting', current_process().name)


def process_jobs(cache_id: str) -> dict:
    start = time.perf_counter()
    job_texts = get_job_text_from_mongo_cache(cache_id)
    end = time.perf_counter()
    print(f'Finished in {round(end - start, 4)} seconds')

    start = time.perf_counter()
    # Multiprocessing for signal job keywords
    keywords_list = Manager().list()
    jobs = [Process(target=get_job_keywords_list, args=(keywords_list, text)) for text in job_texts.values()]
    for job in jobs:
        job.start()
    for j in jobs:
        j.join()

    # Add keywords to result dict
    keywords_dict = dict()
    for job_keywords in keywords_list:
        for key in job_keywords:
            if key not in keywords_dict:
                keywords_dict[key] = job_keywords[key]
            else:
                for keyword in job_keywords[key]:
                    keywords_dict[key].append(keyword)

    # Standardize keywords
    for value in keywords_dict.values():
        for i, j in enumerate(value):
            for k, v in standard_words.items():
                if j in v:
                    value[i] = k

    # Count and sort keywords
    for key in keywords_dict:
        keywords_dict[key] = OrderedDict(Counter(keywords_dict[key]).most_common())

    end = time.perf_counter()
    print(f'Finished in {round(end - start, 4)} seconds')
    return json.dumps(keywords_dict)  # convert to json to keep the order during transaction


def get_job_text_from_mongo_cache(cache_id: str) -> str:
    job = MongoManager().find_by_cache_id(cache_id)
    return job['data']


def get_job_keywords_list(keywords_list, job_text):
    keywords = generate_key_words_from_job_desc(job_text)
    keywords_list.append(keywords)

