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
from jingfen.items import ClassItem, ProductItem
from run import JingFenClass
import better_exceptions

better_exceptions.MAX_LENGTH = None


class JingfenjieSpider(Commons, scrapy.Spider):
    name = 'shoye'
    allowed_domains = ['jd.com']
    uri = "https://qwd.jd.com"
    jingfen_url = "%s/fcgi-bin/qwd_activity_list?env=3" % uri
    jingfen_product_bonus_url = "%s/fcgi-bin/qwd_searchitem_ex?skuid={}" % uri
    jingfen_product_ticket_url = "%s/fcgi-bin/qwd_coupon_query?sku={}" % uri
    start_urls = [jingfen_url]

    def __init__(self, name=None, **kwargs):
        # if name is not None:
        #     self.name = name
        # kwargs.pop('_job')
        super(JingfenjieSpider, self).__init__()
        self.common = Common()
        self.headers = {
            'Accept': "application/json",
            'Referer': "https://qwd.jd.com/",
            'Cache-Control': "no-cache",
        }

    def parse(self, response):
        response_data = json.loads(response.body_as_unicode())
        if not response_data:
            logger.warning("respone is %s") % response_data
            return
        if response_data and 'act' in response_data and not response_data['act']:
            logging.warning("return datas is None")
            return
        for data in response_data['act']:
            name = data['name']
            sub_name = data['subName']
            jd_uid = data['uniqueId']
            pic_url = data['picUrl']
            url = data['desUrl']
            product_sku_ids = data['skuIds']
            type = data['type']
            come_from = "product_class"
            item = dict(
                name=name,
                jd_uid=jd_uid,
                pic_url=pic_url,
                url=url,
                product_sku_ids=product_sku_ids,
                sub_name=sub_name,
                type=type,
                come_from=come_from)
            if product_sku_ids:
                for sku_str in product_sku_ids.split(','):
                    yield scrapy.Request(
                        self.jingfen_product_bonus_url.format(sku_str),
                        callback=self.parse_products_bonus_data,
                        meta={
                            "jd_uid": jd_uid,
                            "sku_str": sku_str,
                            "class_name": name
                        })
            yield item

    def parse_products_bonus_data(self, response):
        """
        抓取商品信息
        :param self:
        :param sku_ids:
        :return:
        """
        item = ProductItem()
        products_data = json.loads(response.body_as_unicode())
        jd_uid = response.meta['jd_uid']
        class_name = response.meta['class_name']

        if not products_data or products_data['msg'] != 'success':
            logger.warning("[%s]respone is error" % (jd_uid))
            return
        if 'sku' in products_data and not products_data['sku']:
            logger.warning("this class sku is None: %s" % jd_uid)
            return
        for one_product in products_data['sku']:
            item['title'] = one_product["title"]
            item['sku'] = one_product['skuid']
            item['spu'] = one_product['spuid']
            item['price'] = one_product['price']
            item['bonus_rate'] = self.common.holds_item_bonus_rate(one_product)
            item['prize_amout'] = one_product['commissionprice']
            item['image_url'] = one_product['skuimgurl']
            item['url'] = one_product['skuurl']
            item['good_come'] = one_product['goodCom']
            yield scrapy.Request(
                self.jingfen_product_ticket_url.format(item['sku']),
                # self.jingfen_product_ticket_url.format('22086779314'),
                callback=self.parse_products_ticket_data,
                meta={
                    "item": deepcopy(item),
                    "jd_uid": jd_uid,
                    "sku": item['sku'],
                    "class_name": class_name
                })
        pass

    def parse_products_ticket_data(self, response):
        """
        获取商品优惠券信息
        :param response:
        :return:
        """
        item = deepcopy(response.meta['item'])
        jd_uid = response.meta['jd_uid']
        sku = response.meta['sku']
        class_name = response.meta['class_name']
        item['come_from'] = "product_detail"
        jingfen_class = JingFenClass.query.filter_by(jd_uid=jd_uid).first()
        if not jingfen_class:
            logger.info("%s has not in class, please add it" % jd_uid)
            jingfen_class = JingFenClass(name=class_name, jd_uid=jd_uid)
            # Commons.save(jingfen_class)
            jingfen_class.save(jingfen_class)
        jingfen_class = JingFenClass.query.filter_by(jd_uid=jd_uid).first()
        item['jingfen_class_id'] = jingfen_class.id
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
            # print item
            yield item
