# coding:utf-8
from __future__ import unicode_literals

import os
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')
client = redis.StrictRedis(connection_pool=pool)

if __name__ == '__main__':
    for i in range(512):
        client.hset("hello", str(i), str(i))
    print(client.object("encoding", "hello"))  # 获取对象的存储结构

    client.hset("hello", "512", "512")
    print(client.object("encoding", "hello"))  # 再次获取对象的存储结构

    """
    验证小对象存储的边界 hset 超过512个元素要使用标准结构
    结果：
    ziplist
    hashtable
    """
