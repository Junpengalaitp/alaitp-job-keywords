from unittest import TestCase

from keywords.keyword_generator import get_job_text_from_mongo_cache


class TestGeJobTextFromMongoCache(TestCase):
    def test_get_job_text_from_mongo_cache(self):
        jobs = get_job_text_from_mongo_cache('d6c9541ad14d45fc918a22f221ed1aef')
        print(jobs)
        self.assertIsNotNone(jobs)
