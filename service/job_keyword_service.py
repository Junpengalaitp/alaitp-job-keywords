import os
from multiprocessing import Process, Manager

from logger.logger import log
from service.cache_service import get_keyword_cache
from service.spacy_service import spacy_job_keywords, sort_keywords_by_category, get_keyword_by_category
from util.timer import timeit


@timeit
def get_job_keyword_dict(job_description_dict: dict) -> dict:
    keyword_dto_list = Manager().list()  # list data structure for multiprocessing
    process_list = [Process(target=process_one_job, args=(job_id, job_description['jobDescriptionText'], keyword_dto_list))
                    for job_id, job_description in job_description_dict.items()]

    multiprocessing_in_chunks(process_list)

    keyword_idx_by_job = {job_keyword_dto.job_id: job_keyword_dto.get_keyword_list() for job_keyword_dto in keyword_dto_list}
    log.debug(f"keyword_idx_by_job complete: length: {len(keyword_idx_by_job)}")
    keyword_category_order = get_keyword_by_category(keyword_dto_list)

    keyword_category_order = sort_keywords_by_category(keyword_category_order)

    # log.debug(f"keyword_category_order: {keyword_category_order}")

    return {"keywordIndexByJob": keyword_idx_by_job, "orderedKeywordByCategory": keyword_category_order}


def process_one_job(job_id, job_description_text, keyword_dto_list):
    job_keyword_dto = get_keyword_cache(job_id)
    if job_keyword_dto:
        keyword_dto_list.append(job_keyword_dto)
    else:
        spacy_job_keywords(job_id, job_description_text, keyword_dto_list)


def multiprocessing_in_chunks(process_list: list):
    start_idx = 0
    chunk_size = os.cpu_count()
    while start_idx < len(process_list):
        end_idx = start_idx + chunk_size
        if end_idx >= len(process_list):
            end_idx = len(process_list)
        for process in process_list[start_idx: end_idx]:
            process.start()
        for process in process_list[start_idx: end_idx]:
            process.join()
        start_idx += chunk_size
