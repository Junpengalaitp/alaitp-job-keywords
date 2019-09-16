import json
import time
from collections import Counter, OrderedDict

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


def process_jobs(cache_id: str) -> dict:
    job_texts = get_job_text_from_mongo_cache(cache_id)

    start = time.perf_counter()
    keywords_dict = {}
    for text in job_texts.values():
        keywords = generate_key_words_from_job_desc(text)
        for key in keywords:
            if key not in keywords_dict:
                keywords_dict[key] = keywords[key]
            else:
                for keyword in keywords[key]:
                    keywords_dict[key].append(keyword)

    for value in keywords_dict.values():
        for i, j in enumerate(value):
            for k, v in standard_words.items():
                if j in v:
                    value[i] = k

    for key in keywords_dict:
        keywords_dict[key] = OrderedDict(Counter(keywords_dict[key]).most_common())
    end = time.perf_counter()
    print(f'Finished in {round(end - start, 4)} seconds')
    return json.dumps(keywords_dict)  # convert to json to keep the order during transaction


def get_job_text_from_mongo_cache(cache_id: str) -> str:
    job = MongoManager().find_by_cache_id(cache_id)
    return job['data']


# def get_job_keywords_dict(job_text):
#     keywords = generate_key_words_from_job_desc(job_text)
#     for key in keywords:
#         if key not in keywords_dict:
#             keywords_dict[key] = keywords[key]
#         else:
#             for keyword in keywords[key]:
#                 keywords_dict[key].append(keyword)

