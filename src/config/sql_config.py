from sqlalchemy import create_engine

from src.config.config_server import CONFIG_MAP

SERVER_URL = CONFIG_MAP["spring"]["datasource"]["url"].split("//")[1]
username = CONFIG_MAP["spring"]["datasource"]["username"]
password = CONFIG_MAP["spring"]["datasource"]["password"]

conn = create_engine(f'postgresql://{username}:{password}@{SERVER_URL}', pool_recycle=3600)


