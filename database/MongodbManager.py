from bson.objectid import ObjectId
from pymongo import MongoClient

from config.read_config import get_config


class MongoManager:
    def __init__(self):
        mongo_ip = get_config('MONGODB', 'ip')
        mongo_port = get_config('MONGODB', 'port')
        username = get_config('MONGODB', 'username')
        password = get_config('MONGODB', 'password')
        db = get_config('MONGODB', 'db')
        client = MongoClient(f'mongodb://{username}:{password}@{mongo_ip}', int(mongo_port))
        database = client[db]
        self.collection = database[get_config('MONGODB', 'collection')]

    def find_one_by_obj_id(self, obj_id):
        job = self.collection.find_one({'_id': ObjectId(obj_id)})
        return job

    def find_all(self):
        all_jobs = self.collection.find()
        return [job for job in all_jobs]


