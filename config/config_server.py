import requests

config_server_url = "localhost:8810"


def config_from_config_server():
    r = requests.get(f"http://{config_server_url}/job-keyword/default")
    res = r.json()
    config = {}
    for cfg in res['propertySources']:
        config.update(cfg['source'])
    return config


CONFIG = config_from_config_server()

if __name__ == '__main__':
    print(config_from_config_server())
