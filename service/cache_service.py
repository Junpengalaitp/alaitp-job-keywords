import json

from config.redis_config import redis_template
from dto.job_keyword_dto import JobKeywordDTO
from logger.logger import log

enable_cache = True


def store_keyword_cache(job_keyword_dto: JobKeywordDTO):
    job_id = job_keyword_dto.get_job_id()
    if not enable_cache:
        return
    if keyword_cache_exist(job_id):
        return
    redis_template.set(job_id, job_keyword_dto.to_json())
    log.info(f"stored the keyword_dict of job_id: {job_keyword_dto.job_id} in redis")


def get_keyword_cache(job_id: str):
    if not enable_cache:
        return
    cache = redis_template.get(job_id)
    if cache:
        log.info(f"found the keyword_dict of job_id: {job_id} in redis")
        job_keyword_dict = json.loads(cache)
        return JobKeywordDTO(job_keyword_dict['job_id'], job_keyword_dict['keyword_list'])
    else:
        return None


def keyword_cache_exist(job_id: str):
    cache = redis_template.get(job_id)
    if cache:
        return True
    return False
