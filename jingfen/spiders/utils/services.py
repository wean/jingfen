#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/21 下午10:10

import decimal
class Common(object):

    def __init__(self):
        pass


    def holds_item_bonus_rate(self, item):
        """
        提取返利比例
        """
        bonus_rate = decimal.Decimal(item['comRate']) if 'comRate' in item else 0
        if bonus_rate < 1:
            bonus_rate = decimal.Decimal(bonus_rate * 100)
        elif bonus_rate > 100:
            bonus_rate = decimal.Decimal(bonus_rate / 100)
        return bonus_rate
