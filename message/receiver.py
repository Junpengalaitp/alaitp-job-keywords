from entity.RemotiveJob import RemotiveJob
from logger.logger import log
from service.spacy_service import spacy_job_keyword
from util.json_util import to_obj


def receive_job(channel, method_frame, header_frame, body):
    remotive_job = to_obj(RemotiveJob(), body)
    remotive_job.get_cleaned_description()
    jobKeyword = spacy_job_keyword(remotive_job.id, remotive_job.description_text)
    log.info(jobKeyword)
    channel.basic_ack(delivery_tag=method_frame.delivery_tag)
