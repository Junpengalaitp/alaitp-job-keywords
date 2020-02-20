import time
from collections import Counter
from typing import List, Dict

from keyword_processing.spacy_processing import generate_key_words_from_job_desc
from logger.logger import log
from post_processing.keyword_clean import get_standardized_keywords


# def process_job_description(job_description_list: List[dict]) -> dict:
#     start = time.perf_counter()
#     keywords_list = []
#     for job_description in job_description_list:
#         job_keyword_dict = generate_key_words_from_job_desc(job_description['jobDescriptionText'])
#         # job_description['keyword_processing'] = job_keyword_dict
#         # keywords_list.append((job_description['jobId'], job_keyword))
#         keywords_list.append(job_keyword_dict)
#
#     keywords_dict = combine_result_to_dict(keywords_list)
#
#     get_standardized_keywords(keywords_dict)
#
#     sort_keywords_dict(keywords_dict)
#
#     end = time.perf_counter()
#     log.info(f'Jobs keyword_processing generation finished in {round(end - start, 4)} seconds,')
#     return keywords_dict  # convert to json to keep the order during transaction


def combine_result_to_dict(keywords_list: List[dict]) -> Dict[str, list]:
    """
    Combine multiple job keyword dict result into one dict
    """
    keywords_dict = dict()
    for job_keywords in keywords_list:
        for label in job_keywords:
            if label not in keywords_dict:
                keywords_dict[label] = list(job_keywords[label].values())
            else:
                for keyword in job_keywords[label].values():
                    keywords_dict[label].append(keyword)
    return keywords_dict


def sort_keywords_dict(keywords_dict: dict) -> None:
    # return top 20 keyword_processing
    for standard_name in keywords_dict:
        keywords_dict[standard_name] = dict(Counter(keywords_dict[standard_name]).most_common(20))

