import pika

from config.config_server import CONFIG

HOST = CONFIG["spring.rabbitmq.host"]
PORT = CONFIG["spring.rabbitmq.port"]
USER_NAME = CONFIG["spring.rabbitmq.username"]
PASSWORD = CONFIG["spring.rabbitmq.password"]
KEYWORD_EXCHANGE = CONFIG["keyword.exchange"]
KEYWORD_QUEUE = CONFIG["keyword.queue"]
KEYWORD_KEY = CONFIG["keyword.key"]
JOB_EXCHANGE = CONFIG["job.exchange"]
JOB_QUEUE = CONFIG["job.queue"]
JOB_KEY = CONFIG["job.key"]

credentials = pika.PlainCredentials(USER_NAME, PASSWORD)
conn_params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials)

connection = pika.BlockingConnection(conn_params)
channel = connection.channel()

channel.exchange_declare(KEYWORD_EXCHANGE, durable=True, exchange_type="direct")
channel.queue_declare(KEYWORD_QUEUE, durable=True, arguments={"x-message-ttl": 10000})
channel.queue_bind(KEYWORD_QUEUE, KEYWORD_EXCHANGE, KEYWORD_KEY)

channel.exchange_declare(JOB_EXCHANGE, durable=True, exchange_type="direct")
channel.queue_declare(JOB_QUEUE, durable=True, arguments={"x-message-ttl": 10000})
channel.queue_bind(JOB_QUEUE, JOB_EXCHANGE, JOB_KEY)
