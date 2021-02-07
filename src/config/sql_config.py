from sqlalchemy import create_engine

from src.logger.logger import log
from src.setting.settings import SQL_URL

log.info(f"connecting sql using url: {SQL_URL}")
conn = create_engine(SQL_URL, pool_recycle=3600)


