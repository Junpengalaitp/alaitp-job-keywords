import json
from typing import Optional

from config.redis_config import redis_template
from logger.logger import log

enable_cache = True


def store_keyword_cache(job_id: str, keyword_dict: dict):
    if not enable_cache:
        return
    if get_keyword_cache(job_id):
        return
    redis_template.set(job_id, json.dumps(keyword_dict))
    log.info(f"stored the keyword_dict of job_id: {job_id} in redis")


def get_keyword_cache(job_id: str) -> Optional[dict]:
    if not enable_cache:
        return
    cache = redis_template.get(job_id)
    if cache:
        log.info(f"found the keyword_dict of job_id: {job_id} in redis")
        return json.loads(cache)
    else:
        return None
