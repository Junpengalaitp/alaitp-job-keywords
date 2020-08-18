import json

from src.concurrency.ProcessPool import insert_msg
from src.config.config_server import CONFIG
from src.config.rabbit_config import channel
from src.logger.logger import log

JOB_QUEUE = CONFIG["job.queue"]


def receive_job(channel, method_frame, header_frame, body):
    try:
        job_map = json.loads(body)
    except Exception as e:
        log.error(f"message is invalid: {body}, \nerror: {e}")
        return
    insert_msg(job_map)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def start_messaging():
    channel.basic_consume(JOB_QUEUE, receive_job)
    try:
        log.info("RabbitMQ channel start consuming")
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
