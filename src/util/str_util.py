import re

from bs4 import BeautifulSoup


def no_html_tags_text(html_str: str):
    soup_text = BeautifulSoup(html_str, 'lxml').get_text(separator=' ')
    job_desc = re.sub('\s+', ' ', soup_text).strip()
    return job_desc


def to_str(cls):
    def __str__(self):
        return f"{type(self).__name__}({', '.join(f'{item[0]}={item[1]}' for item in self.__dict__.items())})"
    cls.__str__ = __str__
    cls.__repr__ = __str__
    return cls