# coding:utf-8
from __future__ import unicode_literals

import redis
import json


pool = redis.ConnectionPool(host='127.0.0.1', port='6380')

r = redis.Redis(connection_pool=pool)
# r.pfadd("codehole", "user01")
# r.sadd("codehole", "user01")

# for i in range(100000):
#     r.pfadd("codehole", "user%d" % i)
#     total = r.pfcount("codehole")
# print(total, i+1)


for i in range(10000):
    r.pfadd("code1", "user%d" % i)
    total = r.pfcount("code1")
print(total, i+1)
