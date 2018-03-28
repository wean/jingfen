#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/27 上午12:42
from __future__ import unicode_literals, absolute_import

from .jin_group import JingGroupSpider
from .jingfenjie import JingfenjieSpider
from web.celery import app, TASK_CONFIG

@app.task
def fetch_task_jin_group():
    spider = JingGroupSpider()
    # if spider.platform.crawl_status:
    spider.start_requests()