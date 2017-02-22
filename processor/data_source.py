import configparser

from pymongo import MongoClient


class MongoDataSource:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../songci.conf')
        if 'mongo' not in config:
            raise KeyError('Config section [mongo] not found.')
        config_mongo = config['mongo']

        self._client = MongoClient(config_mongo['MONGO_URI'])
        self._db = self._client[config_mongo['MONGO_DB_SONGCI']]

    def find(self, collection_name, *args, **kwargs):
        collection = self._db[collection_name]
        return (document for document in collection.find(*args, **kwargs))

    def save(self, collection_name, _filter, update):
        self._db[collection_name].update_one(_filter, {'$set': update}, upsert=True)

    def create_index(self, col_name, index_field, **kwargs):
        self._db[col_name].create_index(index_field, name=index_field + '_index', **kwargs)
