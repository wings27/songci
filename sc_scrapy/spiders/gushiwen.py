# -*- coding: utf-8 -*-
import urllib.parse

from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider
from scrapy.spiders import Rule

from sc_scrapy.items import SongCiItem
from sc_scrapy.spiders.spider_utils import ignore_case_re


class GushiwenSpider(CrawlSpider):
    name = "gushiwen"
    allowed_domains = ["gushiwen.org"]
    start_urls = (
        'http://www.gushiwen.org/gushi/songsan.aspx',
        'http://so.gushiwen.org/type.aspx?p=1&x=词',
    )

    rules = (
        Rule(LinkExtractor(allow='/view_.+\\.aspx'), callback='parse_songci'),
        Rule(LinkExtractor(allow=ignore_case_re('/type\\.aspx.*x=' + urllib.parse.quote('词')))),
    )

    def parse_songci(self, response):
        item = SongCiItem()
        item['url'] = response.url
        full_title = response.css('div.son1>h1::text').extract_first()
        if full_title:
            try:
                item['tune_name'], item['title'] = full_title.split('·')
            except ValueError:
                item['title'] = full_title

        son2_p = response.css('div.son2>p')
        for p in son2_p:
            for name, field in {'朝代': 'dynasty', '作者': 'author'}.items():
                if name in p.css('::text').extract_first():
                    item[field] = p.css('::text').extract()[1]
        content = ''.join(response.css('div#cont::text').extract()).strip()
        if content:
            item['content'] = content
        else:
            all_p_texts = son2_p.css('::text').extract()
            try:
                item['content'] = '\n'.join(all_p_texts[all_p_texts.index('原文：') + 1:]).strip()
            except ValueError:
                self.logger.error('Cannot parse item. url=%s', response.url)
        yield item
