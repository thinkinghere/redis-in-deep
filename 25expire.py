# coding:utf-8
from __future__ import unicode_literals

import redis
import random
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')

r = redis.Redis(connection_pool=pool)

r.set('foo-expire', 'bar123')
r.expire('foo-expire', 86400)

r.set('foo123', 'bar123')
r.expireat('foo123', int(time.time()) + random.randint(0, 86400))  # int 时间戳
