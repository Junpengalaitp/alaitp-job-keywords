class KeywordDTO:
    def __init__(self, keyword: str, category: str, start_idx: int, end_idx: int):
        self.keyword = keyword
        self.category = category
        self.start_idx = start_idx
        self.end_idx = end_idx

    def to_dict(self):
        return self.__dict__
