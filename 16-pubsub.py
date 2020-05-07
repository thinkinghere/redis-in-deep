# coding:utf-8
from __future__ import unicode_literals

import os
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')
client = redis.StrictRedis(connection_pool=pool)


if __name__ == '__main__':
    p = client.pubsub()

    p.subscribe("codehole")
    time.sleep(1)
    print(p.get_message())

    client.publish("codehole", "java comes")
    time.sleep(1)
    print(p.get_message())

    client.publish("codehole", "python comes")
    time.sleep(1)
    print(p.get_message())
    print(p.get_message())
