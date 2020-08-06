import pika
from loguru import logger

from config.config_server import CONFIG
from config.rabbit_config import channel

KEYWORD_EXCHANGE = CONFIG["keyword.exchange"]
KEYWORD_KEY = CONFIG["keyword.key"]

properties = pika.BasicProperties(headers={"content_type": "application/json"})


def publish(msg):
    channel.basic_publish(exchange=KEYWORD_EXCHANGE, routing_key=KEYWORD_KEY, body=msg, properties=properties)
    logger.debug(f"published -----> {msg}")
