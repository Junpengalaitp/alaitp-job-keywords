import json

from config.redis_config import redis_template
from dto.job_keyword_dto import JobKeywordDTO
from util.json_util import to_obj, to_json

enable_cache = True


def get_job_search_cache(job_search_id: str):
    cache = redis_template.db(1).hgetall(job_search_id)
    if cache:
        return {k.decode('utf-8'): json.loads(v) for k, v in cache.items()}
    else:
        return None


def store_keyword_cache(job_keyword_dto: JobKeywordDTO):
    job_id = job_keyword_dto.get_job_id()
    if not enable_cache:
        return
    if keyword_cache_exist(job_id):
        return
    redis_template.db(2).set(job_id, to_json(job_keyword_dto))


def get_keyword_cache(job_id: str):
    if not enable_cache:
        return
    cache = redis_template.db(2).get(job_id)
    if cache:
        return to_obj(JobKeywordDTO(), cache)
    else:
        return None


def keyword_cache_exist(job_id: str):
    cache = redis_template.db(2).get(job_id)
    if cache:
        return True
    return False


def store_standard_word_cache(other_word: str, standard_word: str):
    if not enable_cache:
        return
    redis_template.db(3).set(other_word, standard_word)


def get_standard_word_cache(other_word: str) -> str:
    cache = redis_template.db(3).get(other_word)
    if cache:
        return cache.decode("utf-8")
    else:
        return other_word


if __name__ == '__main__':
    cached = get_job_search_cache('0175fd1e-57ea-42c1-a7d3-25d5160bc79a')
    print(type(cached['33ddd82e869037306554e258791b6e1efb1d51bf76ac025439be691daa2971bf']))
