# -*- coding: utf-8 -*-
import scrapy
import dateparser
import datetime
from money_parser import price_str
from dateutil.parser import parse
from functools import partial
from adbot.items import AdbotItem


class UncucSpider(scrapy.Spider):
    name = 'uncuc'
    allowed_domains = ['1cuc.com']
    start_urls = ['https://1cuc.com/']

    level = 0

    def parse(self, response):
        # find by category
        for href in response.xpath(
                '//div[@class="index__catlist hidden-phone"]//div[@class="index__catlist__item i0" or @class="index__catlist__item i1"]//div[@class="title"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_page,
                                 meta={'level': self.level})

    def parse_page(self, response):
        # find by item
        for href in response.xpath('//td[@class="sr-page__list__item_descr"]//h3//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_item)

    def parse_item(self, response):
        item = AdbotItem()
        item['title'] = response.xpath('//div[@class="l-main__content"]//h1[@class="v-title"]//b/text()').extract()
        item['body'] = response.xpath(
            '//div[@class="l-main__content"]//div[@class="v-descr_text"]/text()[preceding-sibling::br and following-sibling::br]').extract()
        item['price'] = {}
        price = response.xpath('//div[@class="l-right hidden-phone"]//div[@class="v-price only"]//b/text()').extract()

        if len(price) == 1:
            price = price[0].replace(" ", "")

            value = price_str(price)
            item['price']['value'] = value

            split_price = price.split(value)
            if len(split_price) == 2:
                item['price']['currency'] = split_price[1]

        date = response.xpath('//div[@class="l-main__content"]//div[@class="v-info"]//small/text()').extract()
        date = date[1]
        date = date.split(':')
        date = date[1]
        # TODO falta convertir a long la fecha
        item['date'] = date

        item['contact'] = {}
        item['contact']['name'] = response.xpath('//div[@class="v-author__info"]//span/text()').extract()
        # TODO falta tomar el numero del usuario
        # item['contact']['phone'] = response.xpath('//div[@class="v-author__info"]//a//strong/text()').extract()
        item['url'] = response.url

        item['images'] = []
        item['images'] = self.parse_images(response)
        print("::item ", item)

        yield item

    def parse_images(self, response):
        images = response.xpath(
            '//img[@class="rev_img"]/attribute::src').extract()

        result = []

        for item in images:
            result.append("https:" + item)

        return result
