# coding:utf-8
from __future__ import unicode_literals

import os
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')
client = redis.StrictRedis(connection_pool=pool)

p = client.pubsub()
p.subscribe("codehole")  # 订阅

# 休眠消费者
# while True:
#     msg = p.get_message()
#     if not msg:
#         time.sleep(1)
#         continue
#     print(msg)

# 阻塞消费者
# 不用休眠 处理消息及时 和blpop原理相同
for msg in p.listen():
    print(msg)
