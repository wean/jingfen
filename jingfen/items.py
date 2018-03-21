# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ClassItem(scrapy.Item):
    f = scrapy.Field()
    # define the fields for your item here like:
    name = f
    jd_uid = f
    sub_name = f
    pic_url = f
    url = f
    type = f
    content_skus = f


class ProductItem(scrapy.Item):
    f = scrapy.Field()
    id = f
    jd_uid = f
    title = f
    sku = f
    spu = f
    price = f
    bonus_rate = f
    prize_amout = f
    image_url = f
    url = f
    link = f
    ticket_id = f
    ticket_total_number = f
    ticket_used_number = f
    ticket_amount = f
    start_time = f
    end_time = f
    ticket_valid = f
    good_come = f
    come_from = f
    jingfen_class_id = f
    group_price = f
    group_prson_number = f