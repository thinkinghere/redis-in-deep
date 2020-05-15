# coding:utf-8
from __future__ import unicode_literals

import redis
import json

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')

r = redis.Redis(connection_pool=pool)
# print r.mget('name1', 'name2', 'aaa')
# print r.exists('name1')  # 1 为存在
# print r.exists('hello')  # 0 是不存在
# print r.get('name1')


# print r.setrange('name', 0, "你好")
# print r.getrange('name',0,100)

# list
# print r.lindex('books', '0')
# print r.lrange('books', '0', "-1")

# 使用yield 对列表元素增量迭代

def redis_list_itre(name):
    """
    :param name: redis列表
    :return yield:
    """
    if r.type(name) == "list":
        list_count = r.llen(name)
        for index in range(list_count):
            yield r.lindex(name, index)
    else:
        print "%s is not list type" % name

# for item in redis_list_itre("books"):
#     print item


# 使用Hash存取Userinfo

def redis_user_info_hash_set():
    user_info = {
        "name": "Ha",
        "age": 18,
    }
    r.hmset('user01', user_info)

# redis_hash()


def redis_user_info_hash_get():
    res = r.hmget('user01', 'name', 'age')
    print(res)


# redis_user_info_hash_get()
client = redis.StrictRedis(connection_pool=pool)

r.zadd('zz', 'n1', 1, 'n2', 2)