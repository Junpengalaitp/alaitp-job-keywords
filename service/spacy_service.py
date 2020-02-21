import os

import spacy

from dto.job_keyword_dto import JobKeywordDTO
from service.cache_service import get_standard_word_cache

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def generate_key_words_from_job_desc(job_id: str, job_desc_text: str) -> JobKeywordDTO:
    doc = nlp(job_desc_text)

    job_keyword_dto = JobKeywordDTO(job_id)

    for ent in doc.ents:
        if len(ent.text) > 1 or ent.text in ('c', 'C', 'R', 'r'):
            standard_word = get_standard_word_cache(ent.text)
            keyword_dict = {"keyword": standard_word, "category": ent.label_, "startIdx": ent.start_char,
                            "endIdx": ent.end_char}
            job_keyword_dto.add_keyword(keyword_dict)

    return job_keyword_dto
