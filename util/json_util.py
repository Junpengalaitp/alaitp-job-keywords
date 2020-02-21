import json


def to_json(obj: object) -> str:
    return json.dumps(obj.__dict__)


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d