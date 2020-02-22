import os
from collections import OrderedDict, Counter

import spacy

from dto.job_keyword_dto import JobKeywordDTO
from logger.logger import log
from service.cache_service import get_standard_word_cache
from util.timer import timeit

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def generate_key_words_from_job_desc(job_id: str, job_desc_text: str, keyword_category_order: dict) -> JobKeywordDTO:
    doc = nlp(job_desc_text)

    job_keyword_dto = JobKeywordDTO(job_id)

    for ent in doc.ents:
        if len(ent.text) > 1 or ent.text in ('c', 'C', 'R', 'r'):
            standard_word = get_standard_word_cache(ent.text)
            keyword_dict = {"keyword": standard_word, "category": ent.label_, "startIdx": ent.start_char,
                            "endIdx": ent.end_char}
            job_keyword_dto.add_keyword(keyword_dict)

            add_keyword_by_category(ent.label_, standard_word, keyword_category_order)

    return job_keyword_dto


def add_keyword_by_category(category: str, keyword: str, keyword_category_order: dict):
    category_map = keyword_category_order[category]
    category_map.append(keyword)


@timeit
def sort_keywords_by_category(keyword_category_order: dict) -> dict:
    for category, keyword_list in keyword_category_order.items():
        counts = Counter(keyword_list)
        log.debug(f"category: {category} and its count: {counts}")
        # sort the list by its count ASC
        sorted_list = sorted(keyword_list, key=lambda x: counts[x])
        # remove duplicates and reverse the order
        unique_desc = OrderedDict()
        while sorted_list:
            word = sorted_list.pop()
            if unique_desc.get(word, 0) == 0:
                unique_desc[word] = 1
        keyword_category_order[category] = list(unique_desc.keys())

    return keyword_category_order

