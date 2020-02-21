from dto.keyword_dto import KeywordDTO


class JobKeywordDTO:
    def __init__(self, job_id: str = None, keyword_list=None):
        if not keyword_list:
            keyword_list = []
        self.job_id = job_id
        self.keyword_list = keyword_list

    def add_keyword(self, keyword_dto: KeywordDTO):
        self.keyword_list.append(keyword_dto)

    def get_keyword_list(self):
        return self.keyword_list

    def get_job_id(self):
        return self.job_id
