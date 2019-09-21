import logging

from unittest import TestCase, skip

from database.MongodbManager import MongoManager


class TestMongoManager(TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_find_one_by_obj_id(self):
        job = MongoManager().find_one_by_obj_id('5d85df6a46c23bf07d7f6ecd')
        print(job)
        self.assertIsNotNone(job)

    def test_find_all(self):
        jobs = MongoManager().find_all()
        print(type(jobs))
        self.assertEqual(934, len(jobs))
