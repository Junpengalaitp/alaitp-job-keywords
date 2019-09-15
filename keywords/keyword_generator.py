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
    keywords_list = []
    for text in job_texts.values():
        keywords_list.append(generate_key_words_from_job_desc(text))
    return keywords_list


def get_job_text_from_mongo_cache(cache_id: str) -> str:
    job = MongoManager().find_by_cache_id(cache_id)
    return job['data']
