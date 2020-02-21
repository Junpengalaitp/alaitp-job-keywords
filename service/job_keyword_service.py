from service.cache_service import get_keyword_cache, store_keyword_cache
from service.spacy_service import generate_key_words_from_job_desc
from util.timer import timeit


@timeit
def get_job_keyword_dict(job_description_list: dict) -> dict:
    keyword_dict = {}
    for job_id, job_description in job_description_list.items():
        job_keyword_dto = get_keyword_cache(job_id)
        if not job_keyword_dto:
            job_keyword_dto = generate_key_words_from_job_desc(job_id, job_description['jobDescriptionText'])
        keyword_dict[job_id] = job_keyword_dto.get_keyword_list()
        store_keyword_cache(job_keyword_dto)

    return keyword_dict  # convert to json to keep the order during transaction


def get_standard_word(word: str) -> str:
    return