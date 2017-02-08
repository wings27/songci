# -*- coding: utf-8 -*-

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

    @property
    def document_generator(self):
        return (document for document in self._collection.find() if document and document['content'])

    def save_collection(self, col_name, col_filter, col_update):
        self._db[col_name].update_one(col_filter, col_update, upsert=True)
