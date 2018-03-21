# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from run import (JingFenClass, Product)
from run import db, app
from run import Commons
import decimal
import better_exceptions

better_exceptions.MAX_LENGTH = None


# Session = sessionmaker(bind=eng)
class JingfenPipeline(Commons, object):
    def process_item(self, item, spider):
        print item
        if item['come_from'] == 'product_class':
            item = self.handle_products_class_item(item)
        elif item['come_from'] == 'product_detail':
            item = self.handle_products_record_item(item)
        return item

    def handle_products_class_item(self, item):
        class_data = item
        self.save_class_data(class_data=class_data)

    def save_class_data(self, class_data):

        one_class = JingFenClass.query.filter_by(
            jd_uid=class_data['jd_uid']).first()
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

    def handle_products_record_item(self, item):
        title = item['title']
        sku = item['sku']
        spu = item['spu']
        price = decimal.Decimal(item['price']) if item['price'] else 0
        bonus_rate = decimal.Decimal(
            item['bonus_rate']) if item['bonus_rate'] else 0
        prize_amout = decimal.Decimal(
            item['prize_amout']) if item['prize_amout'] else 0
        image_url = item['image_url']
        url = item['url']
        good_come = int(item['good_come'])
        jingfen_class_id = item['jingfen_class_id']

        ticket_id = item['ticket_id'] if 'ticket_id' in item else None
        if 'ticket_amount' in item and item['ticket_amount']:
            ticket_amount = decimal.Decimal(item['ticket_amount'])
        else:
            ticket_amount = 0
        if 'ticket_total_number' in item and item['ticket_total_number']:
            ticket_total_number = int(item['ticket_total_number'])
        else:
            ticket_total_number = 0
        if 'ticket_used_number' in item and item['ticket_used_number']:
            ticket_used_number = int(item['ticket_used_number'])
        else:
            ticket_used_number = 0

        link = item['link'] if 'link' in item else None
        if 'start_time' in item and item['start_time']:
            start_time = self.get_datetime_by_timestamp(item['start_time'])
        else:
            start_time = None
        if 'end_time' in item and item['end_time']:
            end_time = self.get_datetime_by_timestamp(item['end_time'])
        else:
            end_time = None

        group_price = decimal.Decimal(
            item['group_price']
        ) if 'group_price' in item and item['group_price'] else 0
        group_prson_number = int(
            item['group_prson_number']
        ) if 'group_prson_number' in item and item['group_prson_number'] else 0

        ticket_valid = item[
            'ticket_valid'] if 'ticket_valid' in item else False
        product = Product.query.filter_by(sku=sku).first()
        if product:
            product.title = title
            product.price = price
            product.bonus_rate = bonus_rate
            product.prize_amout = prize_amout
            product.start_time = start_time
            product.end_time = end_time
            product.spu = spu
            product.image_url = image_url
            product.url = url
            product.link = link
            product.ticket_id = ticket_id
            product.ticket_total_number = ticket_total_number
            product.ticket_used_number = ticket_used_number
            product.ticket_amount = ticket_amount
            product.ticket_valid = ticket_valid
            product.good_come = good_come
            product.jingfen_class_id = jingfen_class_id
            product.group_prson_number = group_prson_number
            product.group_price = group_price
        else:
            product = Product(
                jingfen_class_id,
                title,
                sku,
                price,
                bonus_rate,
                prize_amout,
                start_time=start_time,
                end_time=end_time,
                spu=spu,
                image_url=image_url,
                url=url,
                link=link,
                ticket_id=ticket_id,
                ticket_total_number=ticket_total_number,
                ticket_used_number=ticket_used_number,
                ticket_amount=ticket_amount,
                ticket_valid=ticket_valid,
                good_come=good_come,
                group_price=group_price,
                group_prson_number=group_prson_number)
        self.save(product)
