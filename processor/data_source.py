import configparser

from pymongo import MongoClient
from pymongo import UpdateOne


class MongoDataSource:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../app.conf')
        if 'mongo' not in config:
            raise KeyError('Config section [mongo] not found.')
        config_mongo = config['mongo']

        self._client = MongoClient(config_mongo['MONGO_URI'])
        self._db = self._client[config_mongo['MONGO_DB_SONGCI']]

    def find(self, collection_name, *args, **kwargs):
        return self._db[collection_name].find(*args, **kwargs)

    def save(self, collection_name, _filter, update):
        return self._db[collection_name].update_one(
            _filter, {'$set': update}, upsert=True)

    def save_many(self, collection_name, filter_with_update_list):
        return self._db[collection_name].bulk_write(
            [UpdateOne(_filter, {'$set': update}, upsert=True)
             for (_filter, update) in filter_with_update_list])

    def create_index(self, collection_name, index_field, **kwargs):
        return self._db[collection_name].create_index(
            index_field, name=index_field + '_index', **kwargs)
