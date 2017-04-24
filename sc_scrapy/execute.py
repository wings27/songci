from scrapy.cmdline import execute


def execute_spider(*spiders):
    execute("scrapy crawl".split().extend(spiders))
