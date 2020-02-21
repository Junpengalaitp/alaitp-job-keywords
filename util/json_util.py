import json

import re


def to_json(obj: object) -> str:
    return json.dumps(obj.__dict__)


def to_obj(obj: object, json_str: str):
    dic = json.loads(json_str)
    obj.__dict__.update(dic)
    return obj


camel_pat = re.compile(r'([A-Z])')
under_pat = re.compile(r'_([a-z])')


def camel_to_underscore(name):
    return camel_pat.sub(lambda x: '_' + x.group(1).lower(), name)


def underscore_to_camel(name):
    return under_pat.sub(lambda x: x.group(1).upper(), name)


def convert_json(d, convert):
    new_d = {}
    for k, v in d.iteritems():
        new_d[convert(k)] = convert_json(v, convert) if isinstance(v, dict) else v
    return new_d


def convert_load(*args, **kwargs):
    json_obj = json.load(*args, **kwargs)
    return convert_json(json_obj, camel_to_underscore)


def convert_dump(*args, **kwargs):
    args = (convert_json(args[0], underscore_to_camel),) + args[1:]
    json.dump(*args, **kwargs)
