import spacy

from pre_processing.text_clean import get_cleaned_text

nlp = spacy.load('job_model')


def generate_key_words_from_job_desc(job_desc_text: str) -> dict:
    job_desc_text = get_cleaned_text(job_desc_text)

    doc = nlp(job_desc_text)

    keywords_dict = {}

    for ent in doc.ents:
        keyword_index = str(ent.start_char) + ',' + str(ent.end_char)
        if ent.label_ not in keywords_dict:
            keywords_dict[ent.label_] = {keyword_index: ent.text}
            # keywords_dict[ent.label_] = [ent.text]
        else:
            keywords_dict[ent.label_][keyword_index] = ent.text
            # keywords_dict[ent.label_].append(ent.text)

    return keywords_dict

