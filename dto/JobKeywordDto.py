from util.str_util import to_str


@to_str
class JobKeywordDTO:
    def __init__(self, job_id: str = None, request_id: str = None, keyword_list: list = None):
        if not keyword_list:
            keyword_list = []
        self.job_id = job_id
        self.keyword_list = keyword_list
        self.request_id = request_id

    def add_keyword(self, keyword_dict: dict):
        self.keyword_list.append(keyword_dict)
