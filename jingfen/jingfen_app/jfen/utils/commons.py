#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/12 下午9:40
"""此文件配置通用设施，验证装饰器，url正则路由"""

# 导包
import arrow
import functools
import datetime
from flask import session, g, jsonify
from werkzeug.routing import BaseConverter
from ..utils.response_code import RET
from jingfen_app.models import CLASS_TYPE_MAP

class RegexConverter(BaseConverter):
    """在路由中使用正则表达式进行参数提取的工具"""
    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


def login_required(f):
    """
    验证用户登录的装饰器
    :param f:
    :return:
    """
    # functools让被装饰的函数名称不会改变
    @functools.wraps(f)
    def wrapper(*arges,**kwargs):
        # 从session中获取user_id
        user_id = session.get('user_id')
        if user_id is None:
            return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
        else:
            # 用户已经登录
            g.user_id = user_id
            return f(*arges, **kwargs)
    return wrapper

def now(is_str=False, format="YYYY-MM-DD HH:mm:ss"):
    """
    获取当前时间
    :return:
    """
    now = arrow.now().datetime if not is_str else arrow.now().format(format)

    return now

def get_product_type(product_name=None):
    """
    获取最新产品类型的id
    :return:
    """
    type = len(CLASS_TYPE_MAP) if product_name and product_name not in CLASS_TYPE_MAP else CLASS_TYPE_MAP.get(product_name)
    return type

def str_to_datetime(time_str):
    if isinstance(time_str, str):
        datetime = arrow.get(time_str).datetime
    elif isinstance(time_str, int):
        datetime = arrow.get(str(time_str)[::10]).datetime
    else:
        return
    return datetime


# TODO

# 启动
if __name__ == '__main__':
    pass