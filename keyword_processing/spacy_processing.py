from collections import defaultdict

import spacy

from dto.JobKeywordDTO import JobKeywordDTO
from dto.KeywordDTO import KeywordDTO
from logger.logger import log
from pre_processing.text_clean import get_cleaned_text

nlp = spacy.load('job_model_sm')


def generate_key_words_from_job_desc(job_id: str, job_desc_text: str) -> JobKeywordDTO:
    # job_desc_text = get_cleaned_text(job_desc_text)

    doc = nlp(job_desc_text)
    keyword_dict = defaultdict(dict)

    job_keyword_dto = JobKeywordDTO(job_id)

    for ent in doc.ents:
        keyword_index = str(ent.start_char) + ',' + str(ent.end_char)
        if len(ent.text) > 1 or ent.text in ('c', 'C', 'R', 'r'):
            keyword_dto = KeywordDTO(ent.text, ent.label_, ent.start_char, ent.end_char)
            job_keyword_dto.add_keyword(keyword_dto.to_dict())
            # keyword_dict[ent.label_][keyword_index] = ent.text

    return job_keyword_dto

