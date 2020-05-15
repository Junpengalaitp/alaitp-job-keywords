from config.config_server import CONFIG
from config.rabbit_config import channel
from logger.logger import log

KEYWORD_EXCHANGE = CONFIG["keyword.exchange"]
KEYWORD_KEY = CONFIG["keyword.key"]


def publish(msg):
    channel.basic_publish(exchange=KEYWORD_EXCHANGE, routing_key=KEYWORD_KEY, body=msg)
    log.info(f"published -----> {msg}")