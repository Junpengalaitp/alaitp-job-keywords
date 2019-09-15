import logging
from bson.objectid import ObjectId

from pymongo import MongoClient

from config import read_config


class MongoManager:
    def __init__(self):
        mongo_ip = read_config.get_config('mongodb', 'ip')
        mongo_port = read_config.get_config('mongodb', 'port')
        # username = read_config.get_config('mongodb', 'username')
        # password = read_config.get_config('mongodb', 'password')
        # self.client = MongoClient(f'mongodb://{username}:{password}@{mongo_ip}', mongo_port)
        self.client = MongoClient(f'mongodb://{mongo_ip}', int(mongo_port))

    def find_one_by_obj_id(self, obj_id):
        db = self.client.stackoverflow_jobs_remote
        job = db.software_dev.find_one({'_id': ObjectId(obj_id)})
        return job



