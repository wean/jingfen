#! /usr/bin/python
# -*- coding:utf-8 -*-
# @Time    : 2018/3/27 上午12:25
from celery.schedules import crontab
from datetime import timedelta

BROKER_URL = 'redis://127.0.0.1:6379/2'

CELERY_ACCEPT_CONTENT = ['json', 'pickle']
CELERY_RESULT_SERIALIZER = 'json'

CELERY_EVENT_QUEUE_TTL = 10
CELERY_EVENT_QUEUE_EXPIRES = 15
CELERY_IGNORE_RESULT = True
CELERY_ACKS_LATE = False  # 在任务执行之前就ack，而不是任务执行完毕才ack，防止任务执行时间长，导致队列阻塞
CELERYD_PREFETCH_MULTIPLIER = 0  # 单次获取message的数量，默认值为4，如果配置为0则表示没有限制
CELERY_EAGER_PROPAGATES_EXCEPTIONS = True  # 传播异常
CELERYD_MAX_TASKS_PER_CHILD = 20
CELERY_SEND_TASK_SENT_EVENT = True
CELERY_STORE_ERRORS_EVEN_IF_IGNORED = False

CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = {
    # common settings
    "default": {
        "exchange": "default",
        "routing_key": "default"
    },
    "jing_fen_group": {
        "exchange": "jing_fen_group",
        "routing_key": "jing_fen_group.key"
    },
    "jing_fen_jie": {
        "exchange": "jing_fen_jie",
        "routing_key": "jing_fen_jie.key"
    },
}


def get_spider_task_celery_config(platform_configs):
    configs = {}
    for platform_config in platform_configs:
        queue = platform_config["queue"]
        seconds = platform_config["seconds"]
        configs.update({
            'crawl-watchdog-{name}'.format(name=queue): {
                'task': 'crawl.tasks.fetch_task_{name}'.format(name=queue),
                'options': {
                    'queue': '{queue}'.format(queue=queue)
                },
                'schedule': timedelta(seconds=seconds),
            }
        })
    return configs


CELERYBEAT_SCHEDULE = {}

CELERYBEAT_SCHEDULE.update(
    get_spider_task_celery_config([
        {
            "queue": "jing_fen_group",
            "name": u'拼购',
            "seconds": 24 * 60 * 60
        },
        {
            "queue": "jing_fen_jie",
            "name": u'首页',
            "seconds": 24 * 60 * 60
        },
    ]))
