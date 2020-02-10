from collections import defaultdict

import spacy

from pre_processing.text_clean import get_cleaned_text

nlp = spacy.load('job_model_sm')


def generate_key_words_from_job_desc(job_desc_text: str) -> dict:
    # job_desc_text = get_cleaned_text(job_desc_text)

    doc = nlp(job_desc_text)

    keywords_dict = defaultdict(dict)

    for ent in doc.ents:
        keyword_index = str(ent.start_char) + ',' + str(ent.end_char)
        if len(ent.text) > 1 or ent.text in ('c', 'C', 'R', 'r'):
            keywords_dict[ent.label_][keyword_index] = ent.text

    return keywords_dict

