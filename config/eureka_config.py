import requests
from py_eureka_client import eureka_client

from config.config_server import CONFIG


def connect_eureka(ip, port):
    eureka_client.init(eureka_server=CONFIG['eureka.client.serviceUrl.defaultZone'],
                       app_name="keyword",
                       instance_host=ip,
                       instance_port=port,
                       ha_strategy=eureka_client.HA_STRATEGY_OTHER)


def eureka_service_list():
    r = requests.get(CONFIG['eureka.client.serviceUrl.defaultZone'] + '/apps')
    return r.text


if __name__ == '__main__':
    print(eureka_service_list())
