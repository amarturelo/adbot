# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AdbotItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    title = scrapy.Field()
    body = scrapy.Field()
    category = scrapy.Field()
    tags = scrapy.Field()
    price = scrapy.Field()
    date = scrapy.Field()
    contact = scrapy.Field()
    url = scrapy.Field()
    images = scrapy.Field()
