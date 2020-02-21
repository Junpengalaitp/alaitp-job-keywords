import json

from config.redis_config import redis_template
from dto.job_keyword_dto import JobKeywordDTO
from logger.logger import log
from util.json_util import to_obj, to_json

enable_cache = True


def store_keyword_cache(job_keyword_dto: JobKeywordDTO):
    job_id = job_keyword_dto.get_job_id()
    if not enable_cache:
        return
    if keyword_cache_exist(job_id):
        return
    redis_template.set(job_id, to_json(job_keyword_dto))
    log.info(f"stored the keyword_dict of job_id: {job_keyword_dto.job_id} in redis")


def get_keyword_cache(job_id: str):
    if not enable_cache:
        return
    cache = redis_template.get(job_id)
    if cache:
        log.info(f"found the keyword_dict of job_id: {job_id} in redis")
        return to_obj(JobKeywordDTO(), cache)
    else:
        return None


def keyword_cache_exist(job_id: str):
    cache = redis_template.get(job_id)
    if cache:
        return True
    return False
