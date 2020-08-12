import json

from src.util.str_util import to_str


@to_str
class JobKeywordDTO:
    def __init__(self, job_id: str = None, keyword_list: list = None):
        if not keyword_list:
            keyword_list = []
        self.job_id = job_id
        self.keyword_list = keyword_list
        self.category_list = set()

    def add_keyword(self, keyword_dict: dict):
        self.keyword_list.append(keyword_dict)
        self.category_list.add(keyword_dict["category"])

    def to_json(self):
        """ custom jsonify method, because the set class is not json serializable """
        self.category_list = list(self.category_list)
        return json.dumps(self.__dict__)
