import pika

from concurrency.ProcessPool import insert_msg
from entity.RemotiveJob import RemotiveJob
from util.json_util import to_obj


def receive_job(channel, method_frame, header_frame, body):
    remotive_job = to_obj(RemotiveJob(), body)
    remotive_job.get_cleaned_description()
    insert_msg(remotive_job)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)


def start_messaging():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host="localhost"))
    channel = connection.channel()
    channel.basic_consume('job-topic', receive_job)
    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()
    connection.close()
