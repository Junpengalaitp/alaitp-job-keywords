import json
from typing import Optional

from config.redis_config import redis_template
from dto.JobKeywordDto import JobKeywordDTO
from util.json_util import to_obj

enable_cache = True


def get_job_search_cache(job_search_id: str):
    cache = redis_template.db(1).hgetall(job_search_id)
    if cache:
        return {k.decode('utf-8'): json.loads(v) for k, v in cache.items()}
    else:
        return None


def store_keyword_cache(job_keyword_dto: JobKeywordDTO):
    job_id = job_keyword_dto.job_id
    if not enable_cache:
        return
    if keyword_cache_exist(job_id):
        return
    redis_template.db(2).set(job_id, job_keyword_dto.to_json())


def get_keyword_cache(job_id: str):
    if not enable_cache:
        return
    cache = redis_template.db(2).get(job_id)
    return to_obj(JobKeywordDTO(), cache) if cache else None


def keyword_cache_exist(job_id: str):
    cache = redis_template.db(2).get(job_id)
    if cache:
        return True
    return False


def store_standard_word_cache(other_word: str, standard_word: str):
    redis_template.db(3).set(other_word, standard_word)


def get_standard_word_cache(other_word: str) -> str:
    cache = redis_template.db(3).get(other_word)
    if cache:
        return cache.decode("utf-8")
    else:
        return other_word


def store_standard_category_cache(standard_word: str, standard_category: str):
    redis_template.db(4).set(standard_word, standard_category)


def get_standard_category_cache(standard_word: str) -> Optional[str]:
    cache = redis_template.db(4).get(standard_word)
    if cache:
        return cache.decode("utf-8")
    else:
        return


def get_cached_keyword_dtos(job_id_list):
    cached_keyword_dto_list, cached_keyword_dto_ids = [], []
    if not enable_cache:
        return cached_keyword_dto_list, cached_keyword_dto_ids
    for job_id in job_id_list:
        job_keyword_dto = get_keyword_cache(job_id)
        if job_keyword_dto:
            cached_keyword_dto_list.append(job_keyword_dto)
            cached_keyword_dto_ids.append(job_keyword_dto.job_id)
    return cached_keyword_dto_list, cached_keyword_dto_ids


def get_keyword_cache_keys():
    cache = redis_template.db(2).keys()
    return [c.decode('utf-8') for c in cache] if cache else None


if __name__ == '__main__':
    cached = get_keyword_cache_keys()
    print(len(cached))
    print(cached)
