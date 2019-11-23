import spacy

from pre_processing.text_clean import get_cleaned_text

nlp = spacy.load('job_model')


def generate_key_words_from_job_desc(job_desc_text: str) -> dict:
    job_desc_text = get_cleaned_text(job_desc_text)

    doc = nlp(job_desc_text)

    keywords_dict = {}

    for w in doc.ents:
        if w.label_ not in keywords_dict:
            keywords_dict[w.label_] = [w.text]
        else:
            keywords_dict[w.label_].append(w.text)

    return keywords_dict

