# -*- coding: utf-8 -*-
import scrapy


class PorlalivreSpider(scrapy.Spider):
    name = 'porlalivre'
    allowed_domains = ['porlalivre.com']
    start_urls = ['http://porlalivre.com/']

    def parse(self, response):
        pass
