#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/12 下午11:57
# 导包
import functools
from fire import Fire
import copy
from flask import session, g, jsonify
from werkzeug.routing import BaseConverter
import logging
import redis
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy import String, Boolean, Float
from flask_wtf import CSRFProtect
from flask_session import Session
from logging.handlers import RotatingFileHandler
import arrow
import json
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
import better_exceptions

better_exceptions.MAX_LENGTH = None


# ---------------------------------------------#config------------------------------------------------------------------------#
class Config:
    """
    基本配置类
    """
    # token
    SECRET_KEY = 'TQ343dfsdf34+SDjjojlje343ET+?#$ODFDSFSD'

    # flask_SQLALchemy配置
    #
    # mysql配置
    SQLALCHEMY_DATABASE_URI = 'mysql://zhuchen:zhuchen@118.24.159.168:3306/jingfen_dev'
    #
    # 追踪数据库的修改行为
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 创建 redis参数
    REDIS_HOST = "118.24.159.168"
    REDIS_PORT = 6379
    REDIS_DB = 10

    # flask-session 使用参数
    SESSION_TYPE = "redis"  # 利用redis 来保存session会话
    #
    SESSION_USE_SIGNER = True  # 为sesson_id进行签名
    SESSION_REDIS = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT)  # redis 缓存设置
    #
    PERMANENT_SESSION_LIFETIME = 86400  # session数据的有效期 秒


class DevelopmentConfig(Config):
    """
    开发模式的参数配置
    """
    DEBUG = True


class ProductionConfig(Config):
    """
    生产环境配置
    """
    pass


# 配置参数选择
config = {
    "development": DevelopmentConfig,  # 开发者模式
    "production": ProductionConfig,  # 生产环境
}

# ---------------------------------------------#db and create_app------------------------------------------------------------------------#
db = SQLAlchemy()

db_base = db.Column
# 实现csrf保护
csrf = CSRFProtect()

logging.basicConfig(level=logging.DEBUG)  # 调试debug级
# 创建日志记录器，指明日志保存的路径、每个日志文件的最大大小、保存的日志文件个数上限
file_log_handler = RotatingFileHandler("logs/log", maxBytes=1024 * 1024 * 100, backupCount=10)
# 创建日志记录的格式                 日志等级    输入日志信息的文件名 行数    日志信息
formatter = logging.Formatter('%(levelname)s %(filename)s:%(lineno)d %(message)s')
# 为刚创建的日志记录器设置日志记录格式
file_log_handler.setFormatter(formatter)
# 为全局的日志工具对象（flask app使用的）添加日后记录器
logging.getLogger().addHandler(file_log_handler)


# 创建应用程序实例
def create_app(config_name):
    app = Flask(__name__)
    # 从配置对象中为app设置配置信息
    app.config.from_object(config[config_name])
    # 正则url
    app.url_map.converters["regex"] = RegexConverter
    # 添加csrf保护，类似于设置form.csrf_token()
    csrf.init_app(app)

    Session(app)

    db.init_app(app)
    app.app_context().push()
    # 使用蓝图
    # from .api_1_0 import api as api_1_0_blueprint
    # app.register_blueprint(api_1_0_blueprint, url_prefix="/api/v1.0")
    #
    # from .web_page import html as html_blueprint
    # app.register_blueprint(html_blueprint)

    return app


# ---------------------------------------------#response_code------------------------------------------------------------------------#
# 导包
class RET:
    OK = "0"
    DBERR = "4001"
    NODATA = "4002"
    DATAEXIST = "4003"
    DATAERR = "4004"
    SESSIONERR = "4101"
    LOGINERR = "4102"
    PARAMERR = "4103"
    USERERR = "4104"
    ROLEERR = "4105"
    PWDERR = "4106"
    REQERR = "4201"
    IPERR = "4202"
    THIRDERR = "4301"
    IOERR = "4302"
    SERVERERR = "4500"
    UNKOWNERR = "4501"


error_map = {
    RET.OK: u"成功",
    RET.DBERR: u"数据库查询错误",
    RET.NODATA: u"无数据",
    RET.DATAEXIST: u"数据已存在",
    RET.DATAERR: u"数据错误",
    RET.SESSIONERR: u"用户未登录",
    RET.LOGINERR: u"用户登录失败",
    RET.PARAMERR: u"参数错误",
    RET.USERERR: u"用户不存在或未激活",
    RET.ROLEERR: u"用户身份错误",
    RET.PWDERR: u"密码错误",
    RET.REQERR: u"非法请求或请求次数受限",
    RET.IPERR: u"IP受限",
    RET.THIRDERR: u"第三方系统错误",
    RET.IOERR: u"文件读写错误",
    RET.SERVERERR: u"内部错误",
    RET.UNKOWNERR: u"未知错误",
}

redis_store = redis.StrictRedis(host=Config.REDIS_HOST, port=Config.REDIS_PORT)


class RegexConverter(BaseConverter):
    """在路由中使用正则表达式进行参数提取的工具"""

    def __init__(self, url_map, *args):
        super(RegexConverter, self).__init__(url_map)
        self.regex = args[0]


# ---------------------------------------------#commons------------------------------------------------------------------------#

class Commons(object):
    def __init__(self):
        self.name = None

    def login_required(self, f):
        """
        验证用户登录的装饰器
        :param f:
        :return:
        """

        # functools让被装饰的函数名称不会改变
        @functools.wraps(f)
        def wrapper(*arges, **kwargs):
            # 从session中获取user_id
            user_id = session.get('user_id')
            if user_id is None:
                return jsonify(errno=RET.SESSIONERR, errmsg='用户未登录')
            else:
                # 用户已经登录
                g.user_id = user_id
                return f(*arges, **kwargs)

        return wrapper

    @staticmethod
    def now(is_str=False, format="YYYY-MM-DD HH:mm:ss"):
        """
        获取当前时间
        :return:
        """
        now = arrow.now().datetime if not is_str else arrow.now().format(format)

        return now

    def str_to_datetime(self, time_str):
        if isinstance(time_str, str):
            datetime = arrow.get(time_str).datetime
        elif isinstance(time_str, int):
            datetime = arrow.get(str(time_str)[::10]).datetime
        else:
            return
        return datetime

    @staticmethod
    def save(obj):
        try:
            with app.app_context():
                db.session.add(obj)
                db.session.commit()
        except Exception as e:
            raise Exception(e)
        finally:
            return obj

    def get_datetime_by_timestamp(self, data):
        """
        递归处理时间戳
        :param data:
        :return:
        """
        year = self.now().year
        data = copy.deepcopy(data)
        datetime = self.str_to_datetime(data)
        if datetime and datetime.year != year and len(data) > 0:
            data = data[:len(data) - 1:]
            datetime = self.get_datetime_by_timestamp(data)
        return datetime


# ---------------------------------------------#models------------------------------------------------------------------------#


class BaseModel(Commons, object):
    """模型基类，为每个模型添加创建时间和更新时间"""
    now = Commons.now()
    def __init__(self):
        super(BaseModel, self).__init__()

    create_time = db.Column(db.DATETIME, default=now)
    update_time = db.Column(db.DATETIME, default=now, onupdate=now)


class JingFenClass(BaseModel, db.Model):
    """
    京粉类别
    """
    __tablename__ = "jingfen_class"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    jd_uid = db.Column(db.String(128), unique=True, nullable=True)
    name = db.Column(db.String(128), unique=True, nullable=False)
    sub_name = db.Column(db.String(128), nullable=False, default='')
    url = db.Column(db.String(128), nullable=False, default='')
    pic_url = db.Column(db.String(128), nullable=False, default='')
    type = db.Column(db.Integer, unique=False, nullable=False, default=0)
    content_skus = db.Column(db.String(128), nullable=True, default='')
    products = db.relationship('Product', backref='jingfenclass') # 分类下的所有产品

    def __init__(self, name=None, jd_uid=None):
        self.create_time = self.now
        self.update_time = self.now
        self.name = name
        self.jd_uid = jd_uid

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

        # def __repr__(self):
        #     return self.name


class Product(BaseModel, db.Model):
    """
    京粉产品
    """

    __tablename__ = "jingfen_products"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, index=True)
    title = db.Column(db.String(128), nullable=False, default='')
    sku = db.Column(db.String(128), nullable=True, unique=True, index=True)
    spu = db.Column(db.String(128), nullable=True, unique=True)
    price = db_base(db.Float, nullable=True, default=0)
    bonus_rate = db_base(db.Float, nullable=False, default=0)
    prize_amout = db_base(db.Float, nullable=False, default=0)
    image_url = db_base(db.String(128), nullable=True)
    url = db_base(db.String(128), nullable=True)
    link = db_base(db.String(128), nullable=True)
    ticket_id = db_base(db.String(128), nullable=True)
    ticket_total_number = db_base(db.Integer, nullable=True, default=0)
    ticket_used_number = db_base(db.Integer, nullable=True, default=0)
    ticket_amount = db_base(db.Float, nullable=True, default=0)
    start_time = db_base(db.DateTime, default=Commons.now(), nullable=True)
    end_time = db_base(db.DateTime, default=Commons.now(), nullable=True)
    ticket_valid = db_base(db.Boolean, default=False)
    good_come = db_base(db.Integer, default=0)
    jingfen_class_id = db_base(db.Integer, db.ForeignKey('jingfen_class.id'))
    jingfen_class = relationship('JingFenClass') # jingfen_calss 映射到JingFenClass 这个对象
    group_prson_number = db_base(db.Integer, default=0)
    group_price = db_base(db.Float, default=0)

    def __init__(self, jingfenclass_id, title, sku, price, bonus_rate, prize_amount, start_time=None, end_time=None,
                 spu=None, image_url=None,
                 url=None, link=None, ticket_id=None, ticket_total_number=None, ticket_used_number=None,
                 ticket_amount=None,
                 ticket_valid=None, good_come=None, group_price=0, group_prson_number=0):
        self.jingfen_class_id = jingfenclass_id
        self.title = title
        self.sku = sku
        self.price = price
        self.bonus_rate = bonus_rate
        self.prize_amout = prize_amount
        self.start_time = start_time if start_time else Commons.now()
        self.end_time = end_time if end_time else Commons.now()
        self.spu = spu
        self.image_url = image_url
        self.url = url
        self.link = link
        self.ticket_id = ticket_id
        self.ticket_total_number = ticket_total_number
        self.ticket_used_number = ticket_used_number
        self.ticket_amount = ticket_amount
        self.ticket_valid = ticket_valid
        self.good_come = good_come
        self.group_prson_number = group_prson_number
        self.group_price = group_price

        # pass

        # def __repr__(self):
        #     return self.title

        # def to_dict(self):
        #     product_dict = {
        #         "jd"
        #     }


def manager():
    app = create_app('development')
    db.init_app(app)
    migrate = Migrate(app, db)
    manager = Manager(app)
    manager.add_command('db', MigrateCommand)
    return manager.run()


def get_all():
    return JingFenClass.query.filter_by(type=0).count()


# ---------------------------------------------#view------------------------------------------------------------------------#

app = create_app("development")


@app.route('/index')
def index():
    return "hello"
    pass


if __name__ == '__main__':
    # app.run(debug=True)
    # print get_all()
    # Fire(Commons)
    # Fire(Product)
    manager()
    # manager.run()
    # app.run(host='0.0.0.0', port=9000, debug=True)
