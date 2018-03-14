# -*- coding: utf-8 -*-
import scrapy
import json
import logging
from run import Commons
from copy import deepcopy
logger = logging.getLogger(__name__)
import better_exceptions
better_exceptions.MAX_LENGTH = None
from jingfen.items import JingfenItem


class JingfenjieSpider(Commons, scrapy.Spider):
    name = 'jingfenjie'
    allowed_domains = ['jd.com']
    uri = "https://qwd.jd.com"
    jingfen_url = "%s/fcgi-bin/qwd_activity_list?env=3" % uri
    jingfen_product_bonus_url = "%s/fcgi-bin/qwd_searchitem_ex?skuid={}" % uri
    jingfen_product_ticket_url = "%s/fcgi-bin/qwd_coupon_query?skuid={}" % uri
    start_urls = [jingfen_url]

    def parse(self, response):
        response_data = json.loads(response.body_as_unicode())
        if not response_data:
            logger.warning("respone is %s") % response_data
        if response_data and 'act' in response_data and not response_data['act']:
            logging.warning("return datas is None")
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
                name = name,
                jd_uid = jd_uid,
                pic_url = pic_url,
                url = url,
                product_sku_ids = product_sku_ids,
                sub_name = sub_name,
                type = type,
                come_from = come_from
            )
            sku_str = '%7C'.join(product_sku_ids.split(','))
            yield scrapy.Request(self.jingfen_product_bonus_url.format(sku_str),
                                 callback=self.parse_products_bonus_data,
                                 meta={"class_name": name, "sku_str": sku_str}
                                 )
            yield item

    def parse_products_bonus_data(self, response):
        """
        抓取商品信息
        :param self:
        :param sku_ids:
        :return:
        """
        item = dict()
        products_data = json.loads(response.body_as_unicode())
        class_name = response.meta['class_name']

        if not products_data or products_data['msg'] != 'success':
            logger.warning("[%s]respone is error" % (class_name))
        if 'sku' in products_data and not products_data['sku']:
            logger.warning("this class sku is None| %s" % class_name)
        for one_product in products_data['sku']:
            item['title'] = one_product['title']
            item['sku'] = one_product['skuid']
            item['spu'] = one_product['spuid']
            item['price'] = one_product['price']
            item['bonus_rate'] = one_product['comRate']
            item['prize_amtout'] = one_product['commissionprice']
            item['image_url'] = one_product['skuimgurl']
            item['url'] = one_product['skuurl']
            item['good_come'] = one_product['goodCom']
            yield scrapy.Request(
                self.jingfen_product_ticket_url.format(item['sku']),
                callback=self.parse_products_ticket_data,
                meta={"item": deepcopy(item), "class_name": class_name, "title": item['title']}
            )
        pass

    def parse_products_ticket_data(self, response):
        """
        获取商品优惠券信息
        :param response:
        :return:
        """
        item = deepcopy(response.meta['item'])
        class_name = response.meta['class_name']
        title = response.meta['title']
        item['come_from'] = "product_detail"

        product_ticket_data = json.loads(response.body_as_unicode())
        if not product_ticket_data or product_ticket_data['msg'] != 'query success':
            logger.warning("products_ticket [%s](%s)respone is error" % (class_name, title))
            yield item
        if 'data' in product_ticket_data and not product_ticket_data['data']:
            logger.warning("this class sku is None| %s >> %s " % (class_name, title))
            yield item
        for one_data in product_ticket_data['data']:
            item['ticket_id'] = one_data['couponId']
            item['ticket_numbers'] = one_data['couponNum']
            item['ticket_amount'] = one_data['denomination']
            item['ticket_total_number'] = one_data['couponNum']
            item['ticket_used_number'] = one_data['usedNum']
            item['link'] = one_data['link']
            item['start_time'] = one_data['validBeginTime']
            item['end_time'] = one_data['validEndTime']
            item['ticket_valid'] = True if int(one_data['couponValid']) == 1 else False
            # print item
            yield item




