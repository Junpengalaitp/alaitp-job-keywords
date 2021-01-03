import pika

from src.config.rabbit_config import KEYWORD_EXCHANGE, KEYWORD_KEY, app_channel

properties = pika.BasicProperties(headers={"content_type": "application/json"})


def publish(msg):
    app_channel.basic_publish(exchange=KEYWORD_EXCHANGE, routing_key=KEYWORD_KEY, body=msg, properties=properties)
