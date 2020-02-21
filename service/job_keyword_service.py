from dto.job_keyword_dto import JobKeywordDTO
from service.cache_service import get_keyword_cache, store_keyword_cache
from service.spacy_service import generate_key_words_from_job_desc
from util.timer import timeit


@timeit
def get_job_keyword_dict(job_description_list: dict) -> dict:
    # keyword_dict = {'keywordByJob': {}, 'keywordByLabel': {}}
    keyword_dict = {}
    for job_id, job_description in job_description_list.items():
        job_keyword_dto = get_keyword_cache(job_id)
        # job_keyword_dto = None
        if not job_keyword_dto:
        #     job_keyword_dict = generate_key_words_from_job_desc(job_id, job_description['jobDescriptionText'])
            job_keyword_dto = generate_key_words_from_job_desc(job_id, job_description['jobDescriptionText'])
        keyword_dict[job_id] = job_keyword_dto.get_keyword_list()
    #     job_description['keyword'] = job_keyword_dict
        store_keyword_cache(job_keyword_dto)
    #     keyword_dict['keywordByJob'][job_id] = job_keyword_dict
    #     for label in job_keyword_dict:
    #         if label not in keyword_dict['keywordByLabel']:
    #             keyword_dict['keywordByLabel'][label] = list(job_keyword_dict[label].values())
    #         else:
    #             for keyword in job_keyword_dict[label].values():
    #                 keyword_dict['keywordByLabel'][label].append(keyword)
    #
    # keyword_dict['keywordByLabel'] = get_standardized_keywords(keyword_dict['keywordByLabel'])

    # sort_keywords_dict(keyword_dict['keywordByLabel'])
    # log.info(keyword_dict)
    return keyword_dict  # convert to json to keep the order during transaction