from json import JSONEncoder


class JsonEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class JSONObject:
    def __init__(self, d):
        self.__dict__ = d