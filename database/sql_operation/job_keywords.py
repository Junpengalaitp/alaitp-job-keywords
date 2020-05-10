import pandas as pd

from database.sqlalchemy_manager import conn
from logger.logger import log
from service.cache_service import store_standard_category_cache


def select_all_standard_words() -> pd.DataFrame:
    query = f"""
                SELECT standard_word, other_words, category FROM standard_word
             """
    df = pd.read_sql_query(query, conn)
    log.info(f"select all standard words success: length: {len(df)}")
    return df


if __name__ == '__main__':
    df = select_all_standard_words()
    for row in df.itertuples():
        for other_word in row.other_words.split(','):
            # store_standard_word_cache(other_word, row.standard_word)
            store_standard_category_cache(row.standard_word, row.category)
