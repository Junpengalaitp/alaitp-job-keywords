from collections import Counter, OrderedDict

from database.MongodbManager import MongoManager
from keywords.spacy_processing import generate_key_words_from_job_desc


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
    keywords_dict = {}
    for text in job_texts.values():
        keywords = generate_key_words_from_job_desc(text)
        for key in keywords:
            if key not in keywords_dict:
                keywords_dict[key] = keywords[key]
            else:
                for keyword in keywords[key]:
                    keywords_dict[key].append(keyword)
    for key in keywords_dict:
        keywords_dict[key] = OrderedDict(Counter(keywords_dict[key]).most_common())
    return keywords_dict


def get_job_text_from_mongo_cache(cache_id: str) -> str:
    job = MongoManager().find_by_cache_id(cache_id)
    return job['data']
