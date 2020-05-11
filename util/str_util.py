import re

from bs4 import BeautifulSoup


def no_html_tags_text(html_str: str):
    soup_text = BeautifulSoup(html_str, 'lxml').get_text(separator=' ')
    job_desc = re.sub('\s+', ' ', soup_text).strip()
    return job_desc


def auto_str(cls):
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )
    cls.__str__ = __str__
    return cls