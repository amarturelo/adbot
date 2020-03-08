# -*- coding: utf-8 -*-
from functools import partial
import string
import scrapy
from dateutil.parser import parse

from adbot.items import AdbotItem


class BachecubanoSpider(scrapy.Spider):
    name = 'bachecubano'
    allowed_domains = ['bachecubano.com']
    start_urls = ['https://www.bachecubano.com/']
    level = 0

    def parse(self, response):
        for href in response.xpath(
                '//section[@class="section"]//div[@class="columns"]//div[@class="columns"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_page,
                                 meta={'level': self.level})

    def parse_page(self, response, depth=0):
        for href in response.xpath(
                '//article[@class="media"]//span[contains(@class,"title")]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href), callback=self.parse_item)

        if depth > 0:
            next = response.xpath('//ul[@class="pagination-list"]//a[@rel="next"]/attribute::href').extract()
            if next:
                yield scrapy.Request(response.urljoin(next[0]), callback=partial(self.parse_page, depth=depth - 1))

    def parse_item(self, response):
        item = AdbotItem()
        item['title'] = response.xpath(
            '//div[@class="media"]//div[@class="media-content"]//p[@itemprop="name"]/a/text()').extract()

        item['body'] = self.parse_body(response)

        item['price'] = {}

        currency = response.xpath(
            '//div[@class="card-content"]//div[@class="content has-text-right"]//div[@itemprop="offers"]//meta[@itemprop="priceCurrency"]/attribute::content').extract()
        price = response.xpath(
            '//div[@class="card-content"]//div[@class="content has-text-right"]//div[@itemprop="offers"]//span[@itemprop="price"]/attribute::content').extract()
        if len(price) > 0:
            item['price']['value'] = price[0]
            item['price']['currency'] = currency[0]

        date = response.xpath('//meta[@itemprop="datePublished"]/attribute::content').extract()
        if len(date) > 0:
            date = date[0]
            item['date'] = parse(date)  # dateparser.parse(date, languages=['es'])

        item['contact'] = {}
        item['contact']['name'] = response.xpath(
            '//div[@class="column is-12-tablet is-3-desktop is-2-widescreen is-full-touch"]//p[contains(@class,"title")][1]/text()').extract()
        item['contact']['phone'] = response.xpath(
            '//div[@class="column is-12-tablet is-3-desktop is-2-widescreen is-full-touch"]//span[@itemprop="telephone"]/text()').extract()
        item['url'] = response.url

        item['images'] = []

        images = response.xpath(
            '//div[@class="column is-3-tablet is-3-desktop is-3-widescreen"]//div[@style="display: none;"]//a/attribute::href').extract()
        if len(images) == 0:
            images = response.xpath(
                '//div[@class="column is-3-tablet is-3-desktop is-3-widescreen"]//div[@class="card-image"]//figure[@class="image"]//img/attribute::src').extract()

        item['images'] = self.parse_images(response)

        # print(item)

        yield item

    def parse_body(self, response):
        body = response.xpath('//div[@class="content subtitle box"]/text()').extract()
        result = ""
        for item in body:
            s = item
            printable = set(string.printable)
            filter(lambda x: x in printable, s)
            # s = s.rstrip()
            result += s

        return result

    def parse_images(self, response):
        images = response.xpath(
            '//div[@class="column is-3-tablet is-3-desktop is-3-widescreen"]//div[@style="display: none;"]//a/attribute::href').extract()
        if len(images) == 0:
            images = response.xpath(
                '//div[@class="column is-3-tablet is-3-desktop is-3-widescreen"]//div[@class="card-image"]//figure[@class="image"]//img/attribute::src').extract()

        return images
