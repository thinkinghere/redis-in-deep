# coding:utf-8
from __future__ import unicode_literals

import os
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')
client = redis.StrictRedis(connection_pool=pool)


def key_for(user_id):
    return "account_{}".format(user_id)


def double_account(client, user_id):
    key = key_for(user_id)
    while True:
        client.watch(key)  # 县watch
        value = int(client.get(key))
        value *= 2  # 加倍
        pipe = client.pipeline(transaction=True)
        pipe.multi()  # 开始事务
        pipe.set(key, value)  # 设置新值
        try:
            pipe.execute()  # 执行事务
            break  # 总算成功了
        except redis.WatchError as e:
            print(e)
            continue  # 事务被打断了，重试
    return int(client.get(key))  # 重新获取余额


if __name__ == '__main__':
    user_id = "abc"
    client.setnx(key_for(user_id), 100)  # setnx 做初始化 setnx(key, value)
    print(double_account(client, user_id))
