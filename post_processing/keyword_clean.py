import logging
import re

import requests

from static.constants import standard_words_map

standard_word_list = list(standard_words_map.keys())


def standardize_keywords(keyword_dict: dict):
    for key, keyword_list in keyword_dict.items():
        for index, keyword in enumerate(keyword_list):
            if keyword not in standard_word_list:
                standard_word = get_standard_word(keyword)
                keyword_list[index] = standard_word


def get_standard_word(keyword: str) -> str:
    r = requests.get(f"http://127.0.0.1:8812/standardize-word/{keyword}")
    standard_word = r.text
    logging.info(f"standardize word: {keyword} to {standard_word}")
    return standard_word


def clean_punctuations(keywords_list: list) -> list:
    return [re.sub(r"[^a-zA-Z0-9.-/]+", ' ', keyword) for keyword in keywords_list]


if __name__ == '__main__':
    # word_list = ['react', 'react.js', 'Node', 'React.js']
    # standardize_keywords(word_list)
    # print(word_list)
    word = 'Node'
    s_word = get_standard_word(word)
    print(s_word)
