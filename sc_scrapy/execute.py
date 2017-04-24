from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings


def execute_spider(spider_class):
    process = CrawlerProcess(get_project_settings())

    process.crawl(spider_class)
    process.start()
