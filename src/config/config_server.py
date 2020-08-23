"""
Manual implementation of spring cloud config, request config on app start and store them in cache
"""
import sys

import requests

from src.logger.logger import log


def config_from_config_server():
    env = sys.argv[1]
    config_server_url = sys.argv[2]
    config_server_env_url = f"http://{config_server_url}/job-keyword/{env}"
    log.info(f"get config from {config_server_env_url}")
    r = requests.get(config_server_env_url)
    res = r.json()
    config = {}
    for cfg in res['propertySources']:
        config.update(cfg['source'])
    return config


CONFIG = config_from_config_server()