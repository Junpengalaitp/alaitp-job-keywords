import redis
from redis import Redis

from src.config.config import REDIS_URL
from src.logger.logger import log


class RedisTemplate:
    # Apply singleton
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self):
        log.info(f"connecting redis using url: {REDIS_URL}")
        self.co_occurrence = redis.ConnectionPool.from_url(url=REDIS_URL, db=0)
        self.job_search_pool = redis.ConnectionPool.from_url(url=REDIS_URL, db=1)
        self.job_keyword_pool = redis.ConnectionPool.from_url(url=REDIS_URL, db=2)
        self.standard_word_pool = redis.ConnectionPool.from_url(url=REDIS_URL, db=3)
        self.standard_category_pool = redis.ConnectionPool.from_url(url=REDIS_URL, db=4)

    def db(self, db: int) -> Redis:
        if db == 0:
            return Redis(connection_pool=self.co_occurrence)
        if db == 1:
            return Redis(connection_pool=self.job_search_pool)
        if db == 2:
            return Redis(connection_pool=self.job_keyword_pool)
        if db == 3:
            return Redis(connection_pool=self.standard_word_pool)
        if db == 4:
            return Redis(connection_pool=self.standard_category_pool)


redis_template = RedisTemplate()
