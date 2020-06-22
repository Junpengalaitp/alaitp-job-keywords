import os

import spacy

from dto.JobKeywordDto import JobKeywordDTO
from message.publisher import publish
from service.cache_service import get_standard_word_cache, get_standard_category_cache, store_keyword_cache, \
    get_keyword_cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def generate_job_keyword(job_id: str, job_desc_text: str, request_id: str) -> None:
    # first try if job keyword cache exists
    job_keyword_dto = get_keyword_cache(job_id)
    if job_keyword_dto is None:
        job_keyword_dto = spacy_job_keyword(job_id, job_desc_text)
        # store job keywords in redis, key: job_id
        store_keyword_cache(job_keyword_dto)

    # set request id to job keywords and publish to mq
    job_keyword_dto.request_id = request_id
    publish(job_keyword_dto.to_json())


def spacy_job_keyword(job_id: str, job_desc_text: str) -> JobKeywordDTO:
    doc = nlp(job_desc_text)
    job_keyword_dto = JobKeywordDTO(job_id)
    for ent in doc.ents:
        keyword = ent.text
        if len(keyword) > 1 or keyword in ('c', 'C', 'R', 'r'):
            # filter out the keywords with punctuation in both ends except '.Net', 'C++', 'C#'
            if (not keyword[-1].isalnum() and (keyword[-1] not in ('+', '#'))) or (
                    not keyword[0].isalnum() and keyword[:2].upper() != '.N'):
                # log.debug(f"keyword with punctuation in the end filtered: {keyword}")
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