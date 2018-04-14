# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from elasticsearch import Elasticsearch

class AdbotPipeline(object):
    
    es =  Elasticsearch("http://10.3.201.213:9200")

    def open_spider(self, spider):
        print(self.es.info())

    def process_item(self, item, spider):
        res = es.index(index="ad-index", doc_type='ad', id=1, body=item)
        print("MARTURELO")

        return item
