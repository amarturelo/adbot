# -*- coding: utf-8 -*-
import scrapy


class UncucSpider(scrapy.Spider):
    name = 'uncuc'
    allowed_domains = ['1cuc.com']
    start_urls = ['https://1cuc.com/']

    depth = 0

    def parse(self, response):
        for href in response.xpath('//div[@class="index__catlist hidden-phone"]//div[@class="index__catlist__item i0" or @class="index__catlist__item i1"]//div[@class="title"]//a/attribute::href').extract():
            print(href)
            #yield scrapy.Request(response.urljoin(href), callback=partial(self.parse_page,depth = int(self.depth)))
