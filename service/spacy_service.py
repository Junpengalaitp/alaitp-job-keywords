import os
import sys

import spacy

from dto.job_keyword_dto import JobKeywordDTO
from dto.keyword_dto import KeywordDTO

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def generate_key_words_from_job_desc(job_id: str, job_desc_text: str) -> JobKeywordDTO:
    # job_desc_text = get_cleaned_text(job_desc_text)

    doc = nlp(job_desc_text)

    job_keyword_dto = JobKeywordDTO(job_id)

    for ent in doc.ents:
        if len(ent.text) > 1 or ent.text in ('c', 'C', 'R', 'r'):
            keyword_dto = KeywordDTO(ent.text, ent.label_, ent.start_char, ent.end_char)
            job_keyword_dto.add_keyword(keyword_dto.to_dict())
            # keyword_dict[ent.label_][keyword_index] = ent.text

    return job_keyword_dto