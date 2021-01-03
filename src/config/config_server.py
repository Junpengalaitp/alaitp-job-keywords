import yaml
from kubernetes import client, config

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config()

v1 = client.CoreV1Api()
ret = v1.read_namespaced_config_map("alaitp-shared", "default")
config_yml = dict(ret.data)["application-dev.yml"]

CONFIG_MAP = yaml.load(config_yml)

if __name__ == '__main__':
    print(CONFIG_MAP)