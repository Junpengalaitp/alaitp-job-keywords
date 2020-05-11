class BaseJobDto:
    def __init__(self, id=None, url=None, title=None, company_name=None, category=None, description=None):
        self.id = id
        self.url = url
        self.title = title
        self.companyName = company_name
        self.category = category
        self.description = description
        self.description_text = None
