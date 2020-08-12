"""
redis cache operations
"""

from typing import Optional

from src.config.redis_config import redis_template
from src.dto.JobKeywordDto import JobKeywordDTO
from src.util.json_util import to_obj

enable_cache = True


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

