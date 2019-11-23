from keywords.spacy_processing import generate_key_words_from_job_desc
from pre_processing.text_clean import get_cleaned_text


class KeywordGenerator:
    def __init__(self, job_text: str = None):
        self.job_text = get_cleaned_text(job_text)
        self.keyword_dict = self.get_raw_keyword_dict()

    def get_raw_keyword_dict(self) -> dict:
        keyword_dict = generate_key_words_from_job_desc(self.job_text)

        return keyword_dict
