# coding:utf-8
from __future__ import unicode_literals

import redis
import random

pool = redis.ConnectionPool(host='127.0.0.1', port='6381')

r = redis.Redis(connection_pool=pool)

# 构造26字母
CHARS = ''.join([chr(ord('a') + i) for i in range(26)])


def random_string(n):
    """
    构造随机长度的字符串
    """
    chars = []
    for i in range(n):
        idx = random.randint(0, len(CHARS) - 1)
        chars.append(CHARS[idx])
    return ''.join(chars)


users = list(set([random_string(64) for i in range(100000)]))
print('total users', len(users))
users_train = users[:len(users)//2]  # 前一半
users_test = users[len(users)//2:]  # 后一半

r.delete("code")
falses = 0

"""
使用bf.reserve 设置错误率
不使用 bf.reserve，默认的error_rate是 0.01，默认的initial_size是 100。
"""
r.execute_command("bf.reserve", "code", 0.001, 50000)

for user in users_train:
    """
    将前一半添加
    """
    r.execute_command("bf.add", "code", user)

print('all trained')
for user in users_test:
    """
    拿后一半的数据在已经添加的数据中查找
    """
    ret = r.execute_command("bf.exists", "code", user)
    # 使用另一半的作为误差统计
    if ret == 1:
        falses += 1


"""
total users 100000
all trained
586 50000 err percent: 0.01172  # 误判率 1%
"""
print(falses, len(users_test), f'err percent: {falses/len(users_test)}')
