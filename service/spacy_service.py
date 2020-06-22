import os

import spacy

from dto.JobKeywordDto import JobKeywordDTO
from message.publisher import publish
from service.cache_service import get_standard_word_cache, get_standard_category_cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def spacy_job_keyword(job_id: str, job_desc_text: str, request_id: str):
    doc = nlp(job_desc_text)
    job_keyword_dto = JobKeywordDTO(job_id, request_id)
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
    publish(job_keyword_dto.to_json())
    return job_keyword_dto
