# -*- coding: utf-8 -*-
import logging

from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db, collection_name):
        self.client = MongoClient(mongo_uri)
        self.db = self.client[mongo_db]
        self.collection = self.db[collection_name]

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB', 'songci'),
            collection_name=crawler.settings.get('MONGO_SONGCI_COLLECTION', 'songci_content'),
        )

    def open_spider(self, spider):
        spider.logger.info('Opened spider: %s.', spider)
        spider.logger.info('Using mongo address: %s', self.client.address)

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        self.save_item(item)
        return item

    def save_item(self, item):
        try:
            self.collection.update({'url': item['url']}, dict(item), upsert=True)
        except ServerSelectionTimeoutError as e:
            logging.error('Fail to connect to mongodb. %s', e)
