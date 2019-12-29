from database.sql_operation.job_keywords import select_all_standard_words


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
