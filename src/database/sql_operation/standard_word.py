from loguru import logger

from src.config.sql_config import conn


def select_standard_word(other_word: str) -> str:
    if "'" in other_word:
        return other_word
    query = f"""
                SELECT standard_word
                FROM standard_word 
                WHERE standard_word = '{other_word}'
             """
    try:
        res = conn.execute(query)
        if res.rowcount != 0:
            return res.fetchone()[0]
        else:
            return select_standard_word_by_other_word(other_word)
    except:
        logger.error(f"error word: {other_word}")
        return other_word


def select_standard_word_by_other_word(other_word: str) -> str:
    query = f"""
                SELECT standard_word
                FROM standard_word 
                WHERE other_words LIKE '%%,{other_word},%%'
             """
    res = conn.execute(query)
    if res.rowcount != 0:
        return res.fetchone()[0]
    else:
        return other_word
