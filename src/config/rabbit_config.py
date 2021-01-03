import pika

from src.config.config_server import CONFIG_MAP

HOST = CONFIG_MAP["spring"]["rabbitmq"]["host"]
PORT = CONFIG_MAP["spring"]["rabbitmq"]["port"]
USER_NAME = CONFIG_MAP["spring"]["rabbitmq"]["username"]
PASSWORD = CONFIG_MAP["spring"]["rabbitmq"]["password"]
KEYWORD_EXCHANGE = CONFIG_MAP["keyword"]["exchange"]
KEYWORD_QUEUE = CONFIG_MAP["keyword"]["queue"]
KEYWORD_KEY = CONFIG_MAP["keyword"]["key"]
JOB_EXCHANGE = CONFIG_MAP["job"]["exchange"]
JOB_QUEUE = CONFIG_MAP["job"]["queue"]
JOB_KEY = CONFIG_MAP["job"]["key"]

credentials = pika.PlainCredentials(USER_NAME, str(PASSWORD))
conn_params = pika.ConnectionParameters(host=HOST, port=PORT, credentials=credentials, heartbeat=60,
                                        connection_attempts=2 ** 31 - 1, retry_delay=10)

connection = pika.BlockingConnection(conn_params)
app_channel = connection.channel()

app_channel.exchange_declare(KEYWORD_EXCHANGE, durable=True, exchange_type="direct")
app_channel.queue_declare(KEYWORD_QUEUE, durable=True, arguments={"x-message-ttl": 10000})
app_channel.queue_bind(KEYWORD_QUEUE, KEYWORD_EXCHANGE, KEYWORD_KEY)

app_channel.exchange_declare(JOB_EXCHANGE, durable=True, exchange_type="direct")
app_channel.queue_declare(JOB_QUEUE, durable=True, arguments={"x-message-ttl": 10000})
app_channel.queue_bind(JOB_QUEUE, JOB_EXCHANGE, JOB_KEY)
