import json

from concurrency.ProcessPool import insert_msg
from config.config_server import CONFIG
from config.rabbit_config import channel
from logger.logger import log

JOB_QUEUE = CONFIG["job.queue"]


def receive_job(channel, method_frame, header_frame, body):
    job_map = json.loads(body)
    try:
        insert_msg(job_map["jobId"], job_map["jobDescriptionText"], job_map["requestId"])
    except KeyError:
        log.error(f"message is invalid: {body}")
        return
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def start_messaging():
    channel.basic_consume(JOB_QUEUE, receive_job)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
