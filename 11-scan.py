# coding:utf-8
from __future__ import unicode_literals

import os
import redis
import time

pool = redis.ConnectionPool(host='127.0.0.1', port='6380')

client = redis.StrictRedis(connection_pool=pool)


def mockdata(count):
    """
    填充数据
    """
    for i in range(count):
        client.set("key%d" % i, i)
    print("mockdata success")

    if os.path.exists('rediskeys'):
        os.remove('rediskeys')
        print("rm_redis_keys_from_file success")


def del_few_rediskeys():
    """
    删除少量keys
    """
    taskkey_list = []
    for i in range(10000):
        taskkey_list.append(f"key{i}")
    client.delete(*taskkey_list)  # 删除keys


# cursor_number, keys = client.execute_command('scan', 0, "count", 200000)
# if cursor_number == 0:
#     client.delete(*keys)  # 删除全部keys

# keys = client.execute_command('scan', 0, "count", 1000)
# print(keys)


def pyscan(cursor_number, client):
    """
    Scan 递归读全部的Redis keys并写入文件
    """

    cursor_number, keys = client.execute_command(
        'scan', cursor_number, "count", 100)
    if cursor_number == 0:  # 游标为0 查询完毕
        return - 1
    pyscan(cursor_number, client)  # 递归调用
    # print(cursor_number, keys)
    with open('rediskeys', 'ab+') as f:
        f.writelines([item + b'\n' for item in keys])  # 读取的是二进制的数据 结尾拼接换行
    return 1


# l = ['1', '2', '3', '4', '5', '6', '7']
# with open('rediskeys', 'w+') as f:
#     f.writelines([item + '\n' for item in l])


def rm_redis_keys_from_file():
    start_time = time.time()
    SUCCESS_DELETED = 0
    try:
        with open("rediskeys") as f:
            while True:
                lines = f.readlines(1024 * 1024)  # 分片 默认-1是读取全部
                if not lines:
                    break
                else:
                    taskkey_list = [i.strip()
                                    for i in lines if lines and i.startswith('key')]  # 删除指定前缀的keys
                    SUCCESS_DELETED += client.delete(*taskkey_list)
                print("SUCCESS_DELETED", SUCCESS_DELETED)
    except Exception as e:
        print(e)

    if os.path.exists('rediskeys'):
        os.remove('rediskeys')
        print("rm_redis_keys_from_file success")

    end_time = time.time()
    print(end_time - start_time, SUCCESS_DELETED)


def redis_flush():
    """
    清空当前数据库中的所有key: flushdb
    删除所有数据库中的key: flushall
    """
    client.execute_command("flushdb")


def get_all_keys(cursor, client):
    """
    遍历获取全部的keys
    """
    cursor_number, keys = client.execute_command('scan', cursor, "count", 1000)
    write_redis_keys(keys)
    while True:
        if cursor_number == 0:
            # 结束一次完整的遍历
            break
        cursor_number, keys = client.execute_command(
            'scan', cursor_number, "count", 1000)
        write_redis_keys(keys)


def write_redis_keys(keys):
    """
    Write redis keys to file
    """
    with open('rediskeys', 'ab+') as f:
        f.writelines([item + b'\n' for item in keys])  # 读取的是二进制的数据 结尾拼接换行
    print("write_redis_keys success")


if __name__ == "__main__":
    mockdata(10000)
    get_all_keys(0, client)
    rm_redis_keys_from_file()
    # redis_flush()
    # write_redis_keys(1, client)

    # print(pyscan(0, client))
    # write_redis_keys()
    # rm_redis_keys_from_file()
