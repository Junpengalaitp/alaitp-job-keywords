from py_eureka_client import eureka_client

from config.config_server import CONFIG


def connect_eureka(ip, port):
    eureka_client.init(eureka_server=CONFIG['eureka.client.serviceUrl.defaultZone'],
                       app_name="job-keyword",
                       instance_host=ip,
                       instance_port=port,
                       ha_strategy=eureka_client.HA_STRATEGY_OTHER)
