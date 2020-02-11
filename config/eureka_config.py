from py_eureka_client import eureka_client


def connect_eureka(ip, port):
    eureka_client.init(eureka_server="http://localhost:8811/eureka",
                       app_name="job-keywords",
                       instance_host=ip,
                       instance_port=port,
                       ha_strategy=eureka_client.HA_STRATEGY_OTHER)
