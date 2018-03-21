# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from run import Commons
from copy import deepcopy
from utils.services import Common

logger = logging.getLogger(__name__)
import better_exceptions

better_exceptions.MAX_LENGTH = None
from jingfen.items import ProductItem
from run import JingFenClass
import better_exceptions

better_exceptions.MAX_LENGTH = None


class JingGroupSpider(Commons, scrapy.Spider):
    name = '拼购'
    allowed_domains = ['jd.com']
    uri = "https://qwd.jd.com"
    jingfen_url = "{}/cgi-bin/qwd_pin_gou?pageSize=20&pageIndex={}&cid1=".format(
        uri, 1)
    jingfen_product_bonus_url = "%s/fcgi-bin/qwd_searchitem_ex?skuid={}" % uri
    jingfen_product_ticket_url = "%s/fcgi-bin/qwd_coupon_query?sku={}" % uri
    start_urls = [jingfen_url]

    def __init__(self):
        self.common = Common()
        self.headers = {
            'Accept': "application/json",
            'Referer': "https://qwd.jd.com/",
            'Cache-Control': "no-cache",
        }
        self.jingfen_class = JingFenClass.query.filter_by(jd_uid=1).first()
        self.uri = "https://qwd.jd.com"
        self.jingfen_url = "{}/cgi-bin/qwd_pin_gou?pageSize=20&pageIndex={}&cid1="
        self.jingfen_class_id = self.jingfen_class.id
        self.jd_uid = self.jingfen_class.jd_uid
        self.class_name = self.jingfen_class.name

    def parse(self, response):
        response_data = json.loads(response.body_as_unicode())
        index = response.meta['index'] if 'index' in response.meta else 1
        if not response_data:
            logger.warning("respone is %s") % response_data
            return
        if response_data and 'sku' in response_data and not response_data['sku']:
            logging.warning("return datas is None")
            return
        for one_product in response_data['sku']:
            item = ProductItem()
            item['title'] = one_product["title"]
            item['sku'] = one_product['skuid']
            item['spu'] = one_product['spuid']
            item['price'] = one_product['price']
            item['bonus_rate'] = self.common.holds_item_bonus_rate(one_product)
            item['prize_amout'] = one_product['commissionprice']
            item['image_url'] = one_product['skuimgurl']
            item['url'] = one_product['skuurl']
            item['good_come'] = one_product['goodCom']
            item['group_price'] = one_product['sPinGouPrice']
            item['group_prson_number'] = one_product['sPinGouMemberCount']
            yield scrapy.Request(
                self.jingfen_product_ticket_url.format(item['sku']),
                callback=self.parse_products_ticket_data,
                meta={
                    "item": deepcopy(item),
                    "jd_uid": self.jd_uid,
                    "sku": item['sku'],
                    "class_name": self.class_name
                })
        print(u"当前请求到第[{}]页".format(index)), (self.jingfen_url.format(
            self.uri, index + 1))
        while index < 50:

            try:
                yield scrapy.Request(
                    self.jingfen_url.format(self.uri, index + 1),
                    callback=self.parse,
                    meta={'index': index + 1})
            except Exception as e:
                print e
            index += 1

    def parse_products_ticket_data(self, response):
        """
        获取商品优惠券信息
        """
        item = deepcopy(response.meta['item'])
        sku = response.meta['sku']
        item['come_from'] = "product_detail"
        item['jingfen_class_id'] = self.jingfen_class_id
        product_ticket_data = json.loads(response.body)
        if not product_ticket_data or product_ticket_data['msg'] != 'query success':
            logger.warning("products_ticket (%s)respone is error" % (sku))
            yield item
        if 'data' in product_ticket_data and not product_ticket_data['data']:
            logger.warning("this product [%s] sku is None" % (sku))
            yield item
        for one_data in product_ticket_data['data']:
            item['ticket_id'] = one_data['couponId']
            item['ticket_amount'] = one_data['denomination']
            item['ticket_total_number'] = one_data['couponNum']
            item['ticket_used_number'] = one_data['usedNum']
            item['link'] = one_data['link']
            item['start_time'] = one_data['validBeginTime']
            item['end_time'] = one_data['validEndTime']
            item['ticket_valid'] = True if int(
                one_data['couponValid']) == 1 else False
            yield item
