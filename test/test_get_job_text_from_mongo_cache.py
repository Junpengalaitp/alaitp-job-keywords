from unittest import TestCase

from keywords.keyword_generator import get_all_jobs


class TestGeJobTextFromMongo(TestCase):
    def test_get_job_text_from_mongo(self):
        jobs = get_all_jobs()
        print(jobs)
        self.assertEquals(934, len(jobs))
