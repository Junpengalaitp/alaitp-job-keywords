import os
from multiprocessing import Process, Manager

from loguru import logger

from service.cache_service import get_cached_keyword_dtos
from service.spacy_service import spacy_job_keywords, get_keyword_by_category, \
    top_keywords_by_category
from util.timer import timeit


@timeit
def get_job_keyword_dict(job_description_dict: dict) -> dict:
    # get all cached keyword_dto
    cached_keyword_dto_list, cached_keyword_dto_ids = get_cached_keyword_dtos(job_description_dict.keys())
    logger.debug(f"got {len(cached_keyword_dto_ids)} job_keyword_dto from cache")

    uncached_num = len(job_description_dict) - len(cached_keyword_dto_list)
    # multiprocessing for cpu intensive spacy algorithm
    if uncached_num:
        logger.debug(f"job_keyword_dto of {uncached_num} jobs were not cached, send them to spacy")
        multiprocessing_keyword_dto_list = Manager().list()  # list data structure for multiprocessing
        process_list = [Process(target=spacy_job_keywords,
                        args=(job_id, job_description['jobDescriptionText'], multiprocessing_keyword_dto_list))
                        for job_id, job_description in job_description_dict.items() if job_id not in cached_keyword_dto_ids]
        multiprocessing_in_chunks(process_list)
        keyword_dto_list = cached_keyword_dto_list + list(multiprocessing_keyword_dto_list)
    else:
        keyword_dto_list = cached_keyword_dto_list

    keyword_idx_by_job = {job_keyword_dto.job_id: job_keyword_dto.keyword_list for job_keyword_dto in
                          keyword_dto_list}
    logger.debug(f"keyword_idx_by_job complete: length: {len(keyword_idx_by_job)}")
    keyword_category_order = get_keyword_by_category(keyword_dto_list)

    keyword_category_order = top_keywords_by_category(keyword_category_order)

    # log.debug(f"keyword_category_order: {keyword_category_order}")

    return {"keywordIndexByJob": keyword_idx_by_job, "orderedKeywordByCategory": keyword_category_order}


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
