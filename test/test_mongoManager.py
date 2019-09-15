import unittest
from unittest import TestCase
from database.MongodbManager import MongoManager


class TestMongoManager(TestCase):

    def setUp(self) -> None:
        super().setUp()

    def test_find_one_by_obj_id(self):
        job = MongoManager().find_one_by_obj_id('5d7cc22689005551ffa80114')
        print(job)
        self.assertIsNotNone(job)
