import pika

from src.config.config import RABBITMQ_URL
from src.logger.logger import log

URL = "localhost:5672"
USER_NAME = "junpeng"
PASSWORD = "921102"
KEYWORD_EXCHANGE = "keyword-exchange"
KEYWORD_QUEUE = "keyword-queue"
KEYWORD_KEY = "keyword-key"
JOB_EXCHANGE = "job-exchange"
JOB_QUEUE = "job-queue"
JOB_KEY = "job-key"

log.info(f"connecting rabbitmq using url: {RABBITMQ_URL}")
conn_params = pika.URLParameters(RABBITMQ_URL)

connection = pika.BlockingConnection(conn_params)
app_channel = connection.channel()

app_channel.exchange_declare(KEYWORD_EXCHANGE, durable=True, exchange_type="direct")
app_channel.queue_declare(KEYWORD_QUEUE, durable=True, arguments={"x-message-ttl": 10000})
app_channel.queue_bind(KEYWORD_QUEUE, KEYWORD_EXCHANGE, KEYWORD_KEY)

app_channel.exchange_declare(JOB_EXCHANGE, durable=True, exchange_type="direct")
app_channel.queue_declare(JOB_QUEUE, durable=True, arguments={"x-message-ttl": 10000})
app_channel.queue_bind(JOB_QUEUE, JOB_EXCHANGE, JOB_KEY)

