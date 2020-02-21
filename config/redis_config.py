import redis

from config.config_server import CONFIG

HOST = CONFIG['spring.redis.host']
PORT = CONFIG['spring.redis.port']
DB2 = CONFIG['spring.redis.database']
DB3 = CONFIG['spring.redis.standard.word']

pool_job_keyword = redis.ConnectionPool(host=HOST, port=PORT, db=DB2)

redis_template = redis.Redis(connection_pool=pool_job_keyword)

pool_standard_word = redis.ConnectionPool(host=HOST, port=PORT, db=DB3)

redis_template_db3 = redis.Redis(connection_pool=pool_standard_word)
