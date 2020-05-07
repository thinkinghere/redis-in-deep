# coding:utf-8
from __future__ import unicode_literals

import os
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')

client = redis.StrictRedis(connection_pool=pool)

# 事务 配合管道使用
# 指令较多的时候 将多次IO操作压缩为单次IO操作
pipe = client.pipeline(transaction=True)
pipe.multi()
pipe.incr("books")
pipe.incr("books")
values = pipe.execute()
