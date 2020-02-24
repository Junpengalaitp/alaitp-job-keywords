import os
from collections import OrderedDict, Counter, defaultdict
from multiprocessing import Manager

import spacy

from dto.job_keyword_dto import JobKeywordDTO
from service.cache_service import get_standard_word_cache, store_keyword_cache
from util.timer import timeit

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def spacy_job_keywords(job_id: str, job_desc_text: str, keyword_dto_list):
    doc = nlp(job_desc_text)
    job_keyword_dto = JobKeywordDTO(job_id)
    for ent in doc.ents:
        if len(ent.text) > 1 or ent.text in ('c', 'C', 'R', 'r'):
            standard_word = get_standard_word_cache(ent.text)
            keyword_dict = {"keyword": standard_word,
                            "category": ent.label_,
                            "startIdx": ent.start_char,
                            "endIdx": ent.end_char}
            job_keyword_dto.add_keyword(keyword_dict)

    keyword_dto_list.append(job_keyword_dto)
    store_keyword_cache(job_keyword_dto)


def get_keyword_by_category(job_keyword_dto_list):
    keyword_category_order = defaultdict(list)
    for job_keyword_dto in job_keyword_dto_list:
        job_keyword_list = job_keyword_dto.get_keyword_list()
        for keyword_dict in job_keyword_list:
            keyword_category_order[keyword_dict["category"]].append(keyword_dict["keyword"])
    return keyword_category_order


@timeit
def sort_keywords_by_category(keyword_category_order):
    for category, keyword_list in keyword_category_order.items():
        counts = Counter(keyword_list)
        # log.debug(f"category: {category} and its count: {counts}")
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

