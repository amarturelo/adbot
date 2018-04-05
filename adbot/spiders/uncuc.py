# -*- coding: utf-8 -*-
import scrapy
import dateparser
import datetime
from dateutil.parser import parse
from functools import partial
from adbot.items import AdbotItem

class UncucSpider(scrapy.Spider):
    name = 'uncuc'
    allowed_domains = ['1cuc.com']
    start_urls = ['https://1cuc.com/']

    depth = 0

    def parse(self, response):
        #find by category
        for href in response.xpath('//div[@class="index__catlist hidden-phone"]//div[@class="index__catlist__item i0" or @class="index__catlist__item i1"]//div[@class="title"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href), callback=partial(self.parse_page,depth = int(self.depth)))

    def parse_page(self, response, depth=0):
        #find by item
        print("::category ",response)        
        for href in response.xpath('//td[@class="sr-page__list__item_descr"]//h3//a/attribute::href').extract():
            print("::item ",href)
            yield scrapy.Request(response.urljoin(href), callback=self.parse_item)
        
        #if depth > 0:
            #next = response.xpath('//ul[@class="pagination"]//a[@title="Siguiente"]/attribute::href').extract()
            #if next:
                #yield scrapy.Request(response.urljoin(next[0]), callback=partial(self.parse_page,depth = depth-1))

    def parse_item(self, response):
        item = AdbotItem()
        item['title'] = response.xpath('//div[@class="l-main__content"]//h1[@class="v-title"]//b/text()').extract()
        item['body'] =  response.xpath('//div[@class="l-main__content"]//div[@class="v-descr_text"]/text()[preceding-sibling::br and following-sibling::br]').extract()
        item['price'] = {}
        price = response.xpath('//div[@class="l-right hidden-phone"]//div[@class="v-price only"]//b/text()').extract()
        
        #TODO hay que corregir el parceo del precio pk 2 200 CUC se jode
        if len(price)==1:
            price = price[0].split(" ")
            item['price']['value'] =  price[0]
            item['price']['currency'] =  price[1]

        date = response.xpath('//div[@class="l-main__content"]//div[@class="v-info"]//small/text()').extract()
        date=date[1]
        print("::::::::::leng",len(date))
        print("::::::::::date",date)
        
        
        date = date.split(':')
        date = date[1]
        #TODO falta convertir a long la fecha
        item['date'] = date
        
        item['contact'] = {}
        item['contact']['name'] = response.xpath('//div[@class="v-author__info"]//span/text()').extract()
        #TODO falta tomar el numero del usuario
        #item['contact']['phone'] = response.xpath('//div[@class="v-author__info"]//a//strong/text()').extract()
        item['url'] = response.url

        item['images']=[]
        item['images']= response.xpath('//img[@class="rev_img"]/attribute::src').extract()
        #TODO hacer cuando halla un colach de imagenes
        #if len(images) == 0:
            #item['images']= response.xpath('//div[@class="fotorama__html"]//div[@data-img]/text()').extract()
        print("::item ",item)
        
        yield item