import json
import re

import logging

import requests

from database.sql_operation.job_keywords import select_all_standard_words
from static.constants import standard_words_map


def get_standard_word_map() -> dict:
    df = select_all_standard_words()
    standard_word_map = {}
    for row in df.itertuples():
        other_words = tuple(row.other_words.split(','))
        standard_word_map[row.standard_word] = other_words
    return standard_word_map


if __name__ == '__main__':
    # standard_word_map = get_standard_word_map()
    # print(standard_word_map)
    pass
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


word = 'Node'
s_word = get_standard_word(word)


def get_cleaned_text(text):
    try:
        text = str(text)
        text = text.replace('\n', ' ')  # First of all get rid of line breaking

        text = re.sub(r'\((.*?)\)', ' ', text)  # Remove ('text')
        text = re.sub(r'\[(.*?)\]', ' ', text)  # Remove ['text']
        text = re.sub(r'\{(.*?)\}', ' ', text)  # Remove {'text'}
        text = re.sub(r'</?\w+[^>]*>', ' ', text)  # Remove <'text'>
        text = re.sub(r'\S*@\S*\s?', ' ', text)  # Remove emails
        text = re.sub(r'http\S+', ' ', text)  # Remove URLs

        text = re.sub(r'''[^a-zA-Z0-9.,;'":$]+''', ' ', text)

        text = text.replace(' s ', ' ')  # Remove signal 's' after remove signal quotes

    except Exception as e:
        logging.info('Error occurred while pre_processing the text')
        logging.info(e)

    return text


text = 'node.js'