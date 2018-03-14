# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from run import JingFenClass, db, app, Commons
import better_exceptions
better_exceptions.MAX_LENGTH = None


# Session = sessionmaker(bind=eng)
class JingfenPipeline(object):
    def process_item(self, item, spider):
        print item
        if item['come_from'] == 'product_class':
            item = self.handle_products_class_item(item)
        elif item['come_from'] == 'product_record':
            item = self.handle_products_record_item(item)
        return item

    def handle_products_class_item(self, item):
        class_data = item
        self.save_class_data(class_data=class_data)

    def save_class_data(self, class_data):

        one_class = JingFenClass.query.filter_by(jd_uid=class_data['jd_uid']).first()
        name = class_data['name'],
        pic_url = class_data['pic_url'],
        url = class_data['url'],
        content_skus = class_data['product_sku_ids'],
        sub_name = class_data['sub_name'],
        jd_uid = class_data['jd_uid'],
        type = class_data['type']
        if one_class:
            one_class.name = name
            one_class.pic_url = pic_url
            one_class.url = url
            one_class.content_skus = content_skus
            one_class.sub_name = sub_name
            one_class.type = type
        else:
            one_class = JingFenClass(name)
            one_class.name = name
            one_class.pic_url = pic_url
            one_class.content_skus = content_skus
            one_class.sub_name = sub_name
            one_class.jd_uid = jd_uid
            one_class.url = url
            one_class.type = type
        with app.app_context():
            db.session.add(one_class)
            db.session.commit()

