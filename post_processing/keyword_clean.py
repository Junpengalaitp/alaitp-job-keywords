import logging
import re

from fuzzywuzzy import fuzz

from static.constants import standard_words

standard_word_list = list(standard_words.keys())


# standard_word_list = ['React', 'Node.js']


def standardize_keywords(keyword_dict: dict):
    for key, keyword_list in keyword_dict.items():
        for index, keyword in enumerate(keyword_list):
            if keyword not in standard_word_list:
                standard_word = get_standard_word(keyword)
                keyword_list[index] = standard_word


def get_standard_word(keyword: str) -> str:
    if keyword not in standard_word_list:
        for standard_word in standard_word_list:
            ratio = fuzz.ratio(re.sub(r"[^a-zA-Z0-9+#]+", ' ', standard_word).lower(),
                               re.sub(r"[^a-zA-Z0-9+#]+", ' ', keyword).lower())
            if ratio == 100:
                logging.info(f'standardized {keyword} to {standard_word}')
                keyword = standard_word
    return keyword


def clean_punctuations(keywords_list: list) -> list:
    return [re.sub(r"[^a-zA-Z0-9.-/]+", ' ', keyword) for keyword in keywords_list]


if __name__ == '__main__':
    # word_list = ['react', 'react.js', 'Node', 'React.js']
    # standardize_keywords(word_list)
    # print(word_list)
    word = 'react'
    s_word = get_standard_word(word)
    print(s_word)
