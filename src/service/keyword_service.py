"""Job keyword generation using SpaCy and custom trained model"""
import os
from typing import Any

import spacy

from src.constant.special_word import SPECIAL_WORD
from src.dto.JobKeywordDto import JobKeywordDTO
from src.logger.logger import log
from src.message.publisher import publish
from src.service.cache_service import get_standard_word_cache, get_standard_category_cache, store_keyword_cache, \
    get_keyword_cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def process_job_keywords(job_map: dict) -> Any:
    """Get the job keyword and publish it to mq"""

    job_id = job_map["jobId"]
    description = job_map["jobDescriptionText"]
    request_id = job_map["requestId"]
    job_number = job_map["jobNumber"]
    total_job_count = job_map["totalJobCount"]
    request_end = job_map["requestEnd"]

    job_keyword_dto = generate_job_keyword(job_id, description)
    # set request id to job keywords and publish to mq
    job_keyword_dto.request_id = request_id
    job_keyword_dto.job_number = job_number
    job_keyword_dto.total_job_count = total_job_count
    # when all jobs of this request are complete, send an ending message
    if request_end is True or job_number == total_job_count:
        job_keyword_dto.request_end = True

    publish(job_keyword_dto.to_json())
    log.info(f"published {job_number}/{total_job_count}")


def generate_job_keyword(job_id: str, job_desc_text: str) -> JobKeywordDTO:
    """if job keyword is cache, return the cached value, else generate keywords using SpaCy model"""
    # first try if job keyword cache exists
    job_keyword_dto = get_keyword_cache(job_id)
    # when no cache exists, generate keywords using spacy model
    if job_keyword_dto is None:
        job_keyword_dto = spacy_job_keyword(job_id, job_desc_text)
        # store job keywords in redis, key: job_id
        store_keyword_cache(job_keyword_dto)
    return job_keyword_dto


def spacy_job_keyword(job_id: str, job_desc_text: str) -> JobKeywordDTO:
    """Generate JobKeywordDTO using SpaCy model"""
    doc = nlp(job_desc_text)
    job_keyword_dto = JobKeywordDTO(job_id)
    for ent in doc.ents:
        keyword = ent.text
        if _invalid_word(keyword):
            continue
        standard_word = get_standard_word_cache(keyword)
        standard_category = get_standard_category_cache(standard_word)
        category = ent.label_ if standard_category is None else standard_category
        keyword_dict = {"keyword": standard_word,
                        "category": category,
                        "startIdx": ent.start_char,
                        "endIdx": ent.end_char}
        job_keyword_dto.add_keyword(keyword_dict)
    return job_keyword_dto


def _invalid_word(word: str) -> bool:
    """Filter out invalid words"""
    if len(word) == 1 and word not in SPECIAL_WORD:
        return True
    # filter out the keywords with punctuation in both ends except '.Net', 'C++', 'C#'
    if (not word[-1].isalnum() and (word[-1] not in ('+', '#'))) or (
            not word[0].isalnum() and word[:2].upper() != '.N'):
        return True
    return False
