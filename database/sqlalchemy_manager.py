import logging

from sqlalchemy import create_engine

from config.read_config import get_config
from logger.logger import setup_logging

SERVER_IP = get_config('MYSQL', 'ip')
PORT = get_config('MYSQL', 'port')
DB_NAME = get_config('MYSQL', 'dbname')
username = get_config('MYSQL', 'user')
password = get_config('MYSQL', 'password')

conn = create_engine(
    f'mysql+mysqlconnector://{username}:{password}@{SERVER_IP}:{PORT}/{DB_NAME}?charset=utf8', pool_recycle=3600)

setup_logging()
logger = logging.getLogger("dbLogger")

