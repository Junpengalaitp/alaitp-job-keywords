import pandas as pd

from database.sqlalchemy_manager import conn
from logger.logger import log


def select_all_standard_words() -> pd.DataFrame:
    query = f"""
                SELECT * FROM standard_word
             """
    df = pd.read_sql_query(query, conn)
    log.info(f"select all standard words success: length: {len(df)}")
    return df


if __name__ == '__main__':
    df = select_all_standard_words()
    print(df)
