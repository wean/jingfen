# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from jingfen.items import JingfenItem

class JingfenPipeline(object):
    def process_item(self, item, spider):
        if item['come_from'] == 'product_class':
            item = self.handle_products_class_item(item)
        return item

    def handle_products_class_item(self, item):
        item = JingfenItem()
        item = item
        return item

