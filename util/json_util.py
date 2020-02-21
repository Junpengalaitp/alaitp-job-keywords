import json


def to_json(obj: object) -> str:
    return json.dumps(obj.__dict__)


def to_obj(obj: object, json_str: str):
    dic = json.loads(json_str)
    obj.__dict__.update(dic)
    return obj
