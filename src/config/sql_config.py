from sqlalchemy import create_engine

from src.config.config import SQL_URL
from src.logger.logger import log

log.info(f"connecting sql using url: {SQL_URL}")
conn = create_engine(SQL_URL, pool_recycle=3600)


