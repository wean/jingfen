# -*- coding: utf-8 -*-
import scrapy
import json
import logging
logger = logging.getLogger(__name__)


class JingfenjieSpider(scrapy.Spider):
    name = 'jingfenjie'
    allowed_domains = ['jd.com']
    uri = "https://qwd.jd.com"
    jingfen_url = "%s/fcgi-bin/qwd_activity_list?env=3" % uri
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
            pic_url = data['picUrl']
            url = data['desUrl']
            product_sku_ids = data['skuIds']
            come_from = "product_class"
            item = dict(
                name = name,
                pic_url = pic_url,
                url = url,
                product_sku_ids = product_sku_ids,
                sub_name = sub_name,
                come_from = come_from
            )
            yield item



