import heapq
import os
from collections import OrderedDict, Counter, defaultdict

import spacy

from entity.JobKeywordDto import JobKeywordDTO
from logger.logger import log
from message.receiver import publish
from service.cache_service import get_standard_word_cache, store_keyword_cache, get_standard_category_cache
from util.timer import timeit

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(BASE_DIR, 'spacy_model', 'job_model_sm')

nlp = spacy.load(model_path)


def spacy_job_keywords(job_id: str, job_desc_text: str, keyword_dto_list):
    doc = nlp(job_desc_text)
    job_keyword_dto = JobKeywordDTO(job_id)
    for ent in doc.ents:
        keyword = ent.text
        if len(keyword) > 1 or keyword in ('c', 'C', 'R', 'r'):
            # filter out the keywords with punctuation in both ends except '.Net', 'C++', 'C#'
            if (not keyword[-1].isalnum() and (keyword[-1] not in ('+', '#'))) or (
                    not keyword[0].isalnum() and keyword[:2].upper() != '.N'):
                # log.debug(f"keyword with punctuation in the end filtered: {keyword}")
                continue
            standard_word = get_standard_word_cache(keyword)
            standard_category = get_standard_category_cache(standard_word)
            category = ent.label_ if standard_category is None else standard_category
            keyword_dict = {"keyword": standard_word,
                            "category": category,
                            "startIdx": ent.start_char,
                            "endIdx": ent.end_char}
            job_keyword_dto.add_keyword(keyword_dict)

    keyword_dto_list.append(job_keyword_dto)
    store_keyword_cache(job_keyword_dto)


def spacy_job_keyword(job_id: str, job_desc_text: str):
    doc = nlp(job_desc_text)
    job_keyword_dto = JobKeywordDTO(job_id)
    for ent in doc.ents:
        keyword = ent.text
        if len(keyword) > 1 or keyword in ('c', 'C', 'R', 'r'):
            # filter out the keywords with punctuation in both ends except '.Net', 'C++', 'C#'
            if (not keyword[-1].isalnum() and (keyword[-1] not in ('+', '#'))) or (
                    not keyword[0].isalnum() and keyword[:2].upper() != '.N'):
                # log.debug(f"keyword with punctuation in the end filtered: {keyword}")
                continue
            standard_word = get_standard_word_cache(keyword)
            standard_category = get_standard_category_cache(standard_word)
            category = ent.label_ if standard_category is None else standard_category
            keyword_dict = {"keyword": standard_word,
                            "category": category,
                            "startIdx": ent.start_char,
                            "endIdx": ent.end_char}
            job_keyword_dto.add_keyword(keyword_dict)
    log.info(job_keyword_dto)
    publish(str(job_keyword_dto))
    return job_keyword_dto


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


@timeit
def top_keywords_by_category(keyword_category_order):
    for category, keyword_list in keyword_category_order.items():
        counts = Counter(keyword_list)
        # log.debug(f"category: {category} and its count: {counts}")
        heap = [(-freq, word) for word, freq in counts.items()]
        heapq.heapify(heap)
        keyword_category_order[category] = [heapq.heappop(heap)[1] for _ in range(min(10, len(heap)))]

    return keyword_category_order