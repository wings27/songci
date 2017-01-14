# -*- coding: utf-8 -*-

import configparser

from pymongo import MongoClient

from processor.nlp import VerseProcessor


class MongoImporter:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('../songci.conf')
        if 'mongo' not in config:
            raise KeyError('Config section [mongo] not found.')
        config_mongo = config['mongo']

        self.client = MongoClient(config_mongo['MONGO_URI'])
        self.db = self.client[config_mongo['MONGO_DB_SONGCI']]
        self.collection = self.db[config_mongo['MONGO_SONGCI_COLLECTION']]

    def import_data(self):
        for collection in self.collection.find():
            if collection:
                processor = VerseProcessor(collection['content'])
                result = processor.pre_process().punctuation_cut().emblem_cut()
                return result.verse_list
