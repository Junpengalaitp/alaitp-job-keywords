from unittest import TestCase

from keywords.keyword_generator import process_job, process_jobs


class TestProcessJob(TestCase):
    def test_generate_key_words_from_job_desc(self):
        job_dict = process_job('5d7cc22689005551ffa80114')
        print(job_dict)
        self.assertIsNotNone(job_dict)

    def test_process_jobs(self):
        keyword_list = process_jobs('2cba3dda259a43eaaab2f1f49c0eec89')
        print(keyword_list)
        self.assertIsNotNone(keyword_list)
