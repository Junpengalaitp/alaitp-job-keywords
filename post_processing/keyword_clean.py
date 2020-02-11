import logging
import re
import json

import requests

from static.constants import standard_words_map

standard_word_list = list(standard_words_map.keys())


def get_standardized_keywords(keyword_dict: dict) -> dict:
    r = requests.post(f"http://127.0.0.1:8888/word-standardization/standardize-word", data=json.dumps(keyword_dict))
    standard_word_dict = r.text
    return json.loads(standard_word_dict)


def get_standard_word(keyword: str) -> str:
    r = requests.get(f"http://127.0.0.1:8888/word-standardization/standardize-word/{keyword}")
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
