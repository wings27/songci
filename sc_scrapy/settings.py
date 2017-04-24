# -*- coding: utf-8 -*-

import logging

BOT_NAME = 'sc_scrapy'

SPIDER_MODULES = ['sc_scrapy.spiders']
NEWSPIDER_MODULE = 'sc_scrapy.spiders'

JOBDIR = './out/job_sc_scrapy'

ROBOTSTXT_OBEY = True

FEED_EXPORTERS = {
    'json': 'sc_scrapy.item_exporters.UnicodeJsonItemExporter',
    'jl': 'sc_scrapy.item_exporters.UnicodeJsonLinesItemExporter',

}

CONCURRENT_REQUESTS = 32

ITEM_PIPELINES = {
    'sc_scrapy.pipelines.MongoDBPipeline': 300,
}

MONGO_URI = 'mongo:27017'
MONGO_DB = 'songci'
MONGO_SONGCI_COLLECTION = 'songci_content'

LOG_LEVEL = logging.INFO
