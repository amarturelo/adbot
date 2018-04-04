# -*- coding: utf-8 -*-
import scrapy
import dateparser
from functools import partial
from adbot.items import AdbotItem

class OfertasSpider(scrapy.Spider):
    name = 'ofertas'
    allowed_domains = ['ofertas.cu']
    start_urls = [
        'http://ofertas.cu/'
        ]
    depth = 0    

    def parse(self, response):
        for href in response.xpath('//ul[@class="categories"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                          callback=partial(self.parse_page,depth = int(self.depth)))

    def parse_page(self, response, depth=0):
        print(depth)
        for href in response.xpath('//div[@class="listing list-mode"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_item)
        
        if depth > 0:
            next = response.xpath('//ul[@class="pagination"]//a[@title="Siguiente"]/attribute::href').extract()
            if next:
                yield scrapy.Request(response.urljoin(next[0]), callback=partial(self.parse_page,depth = depth-1))



    def parse_item(self, response):
        item = AdbotItem()
        item['title'] = response.xpath('//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//h2/text()').extract()
        item['body'] = response.xpath('//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="ad-description"]/text()').extract()
        
        item['price'] = {}
        
        price = response.xpath('//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="price"]/text()').extract()
        
        if len(price)==1:
            price = price[0].split(" ")
            item['price']['value'] =  price[0]
            item['price']['currency'] =  price[1]

        date = response.xpath('//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//time/attribute::datetime').extract()
        if len(date) == 1:
            date = date[0]
            item['date'] = dateparser.parse(date, languages=['es'])
        
        item['contact'] = {}
        item['contact']['name'] = response.xpath('//div[@class="ad-reply-options"]//p[@class="lead"]/text()').extract()
        item['contact']['phone'] = response.xpath('//div[@class="ad-reply-options"]//a//strong/text()').extract()
        item['url'] = response.url
        

        yield item


          
        
        
