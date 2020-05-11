from entity.RemotiveJob import RemotiveJob
from util.json_util import to_obj


def receive_job(channel, method_frame, header_frame, body):
    print(to_obj(RemotiveJob(), body))
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
