import spacy

from database.MongodbManager import MongoManager

nlp = spacy.load('job_model')


def generate_key_words_from_job_desc(job_obj_id: str) -> dict:
    job = MongoManager().find_one_by_obj_id(job_obj_id)
    job_desc_text = job['job_desc']

    doc = nlp(job_desc_text)

    keywords_dict = {}

    for w in doc.ents:
        if w.label_ not in keywords_dict:
            keywords_dict[w.label_] = [w.text]
        else:
            keywords_dict[w.label_].append(w.text)

    return keywords_dict
