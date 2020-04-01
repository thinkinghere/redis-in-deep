# coding:utf-8
import time
import redis
import uuid
import json

pool = redis.ConnectionPool(host='127.0.0.1',port='6380')

clinet = redis.Redis(connection_pool=pool)

class attrdict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def delay(msg):
    msg.id = str(uuid.uuid4())  # 保证 value 值唯一
    value = json.dumps(msg)
    retry_ts = time.time() + 5  # 5 秒后重试
    if redis.VERSION[0] < 3:
        clinet.zadd("delay-queue", retry_ts, value)
    else:
        clinet.zadd('delay-queue', {value: retry_ts})

msg = attrdict()

delay(msg)
delay(msg)
delay(msg)

def loop():
    while True:
        # 最多取 1 条
        values = clinet.zrangebyscore("delay-queue", 0, time.time(), start=0, num=1)
        if not values:
            time.sleep(1)  # 延时队列空的，休息 1s
            continue
        value = values[0]  # 拿第一条，也只有一条
        success = clinet.zrem("delay-queue", value)  # 从消息队列中移除该消息
        if success:  # 因为有多进程并发的可能，最终只会有一个进程可以抢到消息
            msg = json.loads(value)
            print(msg)
    print('exit')
loop()
