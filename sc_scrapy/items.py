# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SongCiItem(scrapy.Item):
    url = scrapy.Field()
    tune_name = scrapy.Field()
    title = scrapy.Field()
    dynasty = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field()
