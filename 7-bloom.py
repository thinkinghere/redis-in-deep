# coding:utf-8
from __future__ import unicode_literals

import redis
import json

pool = redis.ConnectionPool(host='127.0.0.1', port='6381')

r = redis.Redis(connection_pool=pool)

# 对已经存在的元素不会出现误判
r.delete("codehole")
for i in range(100000):
    r.execute_command("bf.add", "codehole", "user%d" % i)
    # ret = r.execute_command("bf.exists", "codehole", "user%d" % i)
    # if ret == 0:
    #     print(i)
    #     break

    # 注意 i+1，这个是当前布隆过滤器没见过的
    ret = r.execute_command("bf.exists", "codehole", "user%d" % (i+1))
    if ret == 1:
        print(i)
        break
