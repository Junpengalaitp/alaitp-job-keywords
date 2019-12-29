import re

from fuzzywuzzy import fuzz

from service.standard_word_service import get_standard_word_map

standard_words_map = get_standard_word_map()

if __name__ == '__main__':
    for standard_word, other_words in standard_words_map.items():
        for other_word in other_words:
            ratio = fuzz.partial_ratio(re.sub(r"[^a-zA-Z0-9]+", ' ', standard_word).lower(),
                                       re.sub(r"[^a-zA-Z0-9]+", ' ', other_word).lower())
            print(f'{standard_word} and {other_word} score is {ratio}')
