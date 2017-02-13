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
        self._collection = self._db[config_mongo['MONGO_SONGCI_COLLECTION']]

    def find(self):
        # todo change if statement to db filter, add filter as a parameter.
        # todo make collection name a parameter instead of reading from config.
        return (document for document in self._collection.find() if document and document['content'])

    def save(self, col_name, col_filter, col_update):
        self._db[col_name].update_one(col_filter, {'$set': col_update}, upsert=True)

    def create_index(self, col_name, index_field, **kwargs):
        self._db[col_name].create_index(index_field, name=index_field + '_index', **kwargs)
