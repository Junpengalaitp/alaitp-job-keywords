import pika

from logger.logger import log

connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
channel = connection.channel()

def publish(msg):
    channel.basic_publish(exchange='', routing_key='keyword-topic', body=msg)
    log.info(f"published -----> {msg}")