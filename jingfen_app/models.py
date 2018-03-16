#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/12 下午1:38


from werkzeug.security import generate_password_hash, check_password_hash
import arrow
import json
from run import db



class BaseModel(object):
    """模型基类，为每个模型添加创建时间和更新时间"""
    create_time = db.Column(db.DATETIME, default=now)
    update_time = db.Column(db.DATETIME, default=now, onupdate=now)


class JingFenClass(BaseModel, db.Model):
    """
    京粉产品
    """
    id = db.Column(db.Integer, primary_key=True)
    jd_uid = db.Column(db.String(128), unique=True, nullable=False)
    name = db.Column(db.String(32), unique=True, nullable=False)
    sub_name = db.Column(db.String(32), nullable=False, default='')
    url = db.Column(db.String(100), unique=True, nullable=False, default='')
    pic_url = db.Column(db.String(100), unique=True, nullable=False, default='')
    type = db.Column(db.Integer, unique=True, nullable=False)
    content_skus = db.Column(db.JSON, nullable=False)
    # houses = db.relationship("House", backref="user")  # 用户发布的房子
    # orders = db.relationship("Order", backref="user")  # 用户下的订单

    def to_dict(self):
        """将对象转换为字典数据"""
        class_dict = {
            "class_id": self.id,
            "name": self.name,
            "sub_name": self.sub_name,
            "jd_uid": self.jd_uid,
            "url": self.url,
            "pic_url": self.pic_url,
            "type": self.type,
            "create_time": arrow.get(self.create_time).format(),
            "content_skus": json.loads(self.create_time)

        }
        return class_dict


class

