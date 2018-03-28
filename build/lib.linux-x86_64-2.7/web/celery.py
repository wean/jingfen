#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/27 上午12:08
from __future__ import unicode_literals, absolute_import

import os
from celery import Celery
from jingfen import spiders
import logging

logger = logging.getLogger(__name__)
app = Celery('jingfen')

app.config_from_object('web.celeryconfig')

TASK_CONFIG = {
    # offline platforms
    spiders.JingGroupSpider.name: {
        'crawler_cls': spiders.JingGroupSpider,
        'queue': 'jing_fen_group',
    },
}


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


def _get_task_config(platform_name):
    if platform_name in TASK_CONFIG.keys():
        return TASK_CONFIG[platform_name]
    else:
        return None
