# -*- coding: utf-8 -*-
import scrapy
import string
from dateutil.parser import parse

from adbot.items import AdbotItem


class PorlalivreSpider(scrapy.Spider):
    name = 'porlalivre'
    allowed_domains = ['porlalivre.com']
    start_urls = ['https://porlalivre.com/']

    level = 0

    def parse(self, response):
        for href in response.xpath('//ul[@class="sub-categories list-unstyled"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_page,
                                 meta={'level': self.level})
        # next = response.xpath('//ul[@class="categories"]//a/attribute::href').extract()[1]
        # request = scrapy.Request(response.urljoin(next),
        #                          callback=self.parse_page,
        #                          meta={'level': self.depth})
        # yield request

    def parse_page(self, response):
        level = int(response.meta['level'])
        category = self.categorize(response.request.url)
        for href in response.xpath('//div[@class="listing list-mode"]//a/attribute::href').extract():
            yield scrapy.Request(response.urljoin(href),
                                 callback=self.parse_item,
                                 meta={'category': category})

        if level > 0:
            n = response.xpath('//ul[@class="pagination"]//a[@title="Siguiente"]/attribute::href').extract()
            if n:
                yield scrapy.Request(response.urljoin(n[0]),
                                     callback=self.parse_page,
                                     meta={"level": level - 1})

    def parse_item(self, response):
        item = AdbotItem()
        item['title'] = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//h2/text()').extract()
        # item['body'] = '\n'.join(response.xpath(
        #     '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="ad-description"]/text()').extract())

        item['body'] = self.parse_body(response)

        item['price'] = {}

        price = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="price"]/text()').extract()

        if len(price) == 1:
            price = price[0].split(" ")
            item['price']['value'] = float(price[0].replace("$", "").replace(",", "."))
            item['price']['currency'] = price[1]

        date = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//time/attribute::datetime').extract()
        if len(date) == 1:
            date = date[0]
            item['date'] = parse(date)  # dateparser.parse(date, languages=['es'])

        item['contact'] = {}
        item['contact']['name'] = response.xpath('//div[@class="ad-reply-options"]//p[@class="lead"]/text()').extract()
        item['contact']['phone'] = response.xpath('//div[@class="ad-reply-options"]//a//strong/text()').extract()

        item['images'] = self.parse_images(response)

        item['url'] = response.url
        item['category'] = response.meta['category']

        yield item

    def categorize(self, url):
        for entry in self.map_category.keys():
            if url and entry in url:
                return self.map_category[entry]
        return 0

    def parse_body(self, response):

        # s = "some\x00string. with\x15 funny characters"
        #
        # printable = set(string.printable)
        # filter(lambda x: x in printable, s)

        body = response.xpath(
            '//div[@class="ad-details"]//div[@class="col-xs-12 col-sm-9 listing-wrapper"]//p[@class="ad-description"]/text()').extract()
        result = ""
        for item in body:
            s = item

            printable = set(string.printable)
            filter(lambda x: x in printable, s)
            result += s + "\n"

        return result

    def parse_images(self, response):
        images = response.xpath(
            '//div[@class="row center gallery"]//div[@class="col-xs-6 col-sm-3"]//a/attribute::href').extract()
        result = []
        for item in images:
            result.append("http://ofertas.cu" + item)
        return result
