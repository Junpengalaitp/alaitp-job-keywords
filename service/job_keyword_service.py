from collections import defaultdict

from logger.logger import log
from service.cache_service import get_keyword_cache
from service.spacy_service import spacy_job_keywords, sort_keywords_by_category, add_keyword_by_category
from util.timer import timeit


@timeit
def get_job_keyword_dict(job_description_dict: dict) -> dict:

    keyword_idx_by_job = {}
    keyword_category_order = defaultdict(list)

    for job_id, job_description in job_description_dict.items():
        process_one_job(job_id, job_description['jobDescriptionText'], keyword_idx_by_job, keyword_category_order)

    keyword_category_order = sort_keywords_by_category(keyword_category_order)

    log.debug(f"keyword_category_order: {keyword_category_order}")

    return {"keywordIndexByJob": keyword_idx_by_job, "orderedKeywordByCategory": keyword_category_order}


def process_one_job(job_id, job_description_text, keyword_idx_by_job, keyword_category_order):
    job_keyword_dto = get_keyword_cache(job_id)
    if job_keyword_dto:
        for keyword_dto in job_keyword_dto.keyword_list:
            keyword_idx_by_job[job_id] = job_keyword_dto.get_keyword_list()
            add_keyword_by_category(keyword_dto["category"], keyword_dto["keyword"], keyword_category_order)
    if not job_keyword_dto:
        spacy_job_keywords(job_id, job_description_text, keyword_idx_by_job, keyword_category_order)
