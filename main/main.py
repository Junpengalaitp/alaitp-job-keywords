from multiprocessing import Process

import pika

from config.rabbit_config import on_message
from job_keyword_app import start_test_server


def start_web():
    start_test_server()


def start_messaging():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.basic_consume('job-topic', on_message)

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()

def start_app():
    messaging_process = Process(target=start_messaging)
    web_process = Process(target=start_web)
    messaging_process.start()
    web_process.start()

if __name__ == '__main__':
    start_app()