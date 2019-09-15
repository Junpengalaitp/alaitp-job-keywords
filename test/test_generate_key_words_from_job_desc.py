from unittest import TestCase

from keywords.keyword_generator import generate_key_words_from_job_desc


class Test_Generate_key_words_from_job_desc(TestCase):
    def test_generate_key_words_from_job_desc(self):
        job_dict = generate_key_words_from_job_desc('5d7cc22689005551ffa80114')
        print(job_dict)
        self.assertIsNotNone(job_dict)
