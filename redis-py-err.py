# coding:utf-8
from __future__ import unicode_literals

# redis-py中Python2/3版本的坑

import redis
pool = redis.ConnectionPool(host='127.0.0.1', port='6380')

r = redis.Redis(connection_pool=pool)

# zadd
element1 = "hello world"
score1 = 11

if redis.VERSION[0] < 3:
    print("python2")
    # in python2
    # r.zadd('my-key', element1=score1)
    # r.setex(name, time, value)
    # r.zincrby('test1', 'value', amount=10)
else:
    print('python3')
    """
    def zincrby(self, name, amount, value):
    原生语句 zincrby key increment member
    name ->key 
    amount ->value
    value -> member
    """
    # r.zincrby('test1', 10, 'tom')  # python3和原生的执行顺序一致
    # r.execute_command('zincrby', 'test1', 2, 'jack')

    """
    zadd in python3 is map
    """
    r.zadd('my-key', {element1: score1})
    r.execute_command('zadd', 'books', 9.8, 'python cookbook')
