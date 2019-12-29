from unittest import TestCase

from service.mongo_service import get_all_jobs


class TestGeJobTextFromMongo(TestCase):
    def test_get_job_text_from_mongo(self):
        jobs = get_all_jobs()
        print(jobs)
        self.assertEquals(934, len(jobs))

    def test_get_all_remotive(self):
        jobs = get_all_jobs('remotive')
        print(jobs)
        self.assertEquals(200, len(jobs))

    def test_get_all_wwr(self):
        jobs = get_all_jobs('weworkremotely')
        print(jobs)
        self.assertEquals(227, len(jobs))

    def test_get_all_stackoverflow(self):
        jobs = get_all_jobs('stackoverflow')
        print(jobs)
        self.assertEquals(507, len(jobs))

