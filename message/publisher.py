import pika

from logger.logger import log

def publish(msg):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.basic_publish(exchange='', routing_key='keyword-topic', body=msg)
    log.info(f"published -----> {msg}")