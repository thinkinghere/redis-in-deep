## 使用Docker搭建集群

<!-- ```
docker run --name slave1 -d -p 6382:6379 redis
docker run --name slave2 -d -p 6383:6379 redis
docker run --name slave3 -d -p 6384:6379 redis
``` -->

### Redis 开放远程

```
vim /etc/redis.conf
bind 0.0.0.0
systemctl restart redis
```

### 测试Redis是否响应

```
redis-cli -h 172.18.0.31 -p 6379 ping
PONG
```

### Master

172.18.0.31 

info replication 查看主从关系
connected_slaves 可以查看已连接的slave数量
```
127.0.0.1:6379> info replication
# Replication
role:master
connected_slaves:1
slave0:ip=172.18.0.154,port=6379,state=online,offset=239,lag=0
master_repl_offset:239
repl_backlog_active:1
repl_backlog_size:1048576
repl_backlog_first_byte_offset:2
repl_backlog_histlen:238
```

### Slave

```
127.0.0.1:6379> slaveof 172.18.0.31 6379
```

取消主从
```
127.0.0.1:6379> slaveof no one
```


ref
Sentinel Doc
https://github.com/antirez/redis-doc/blob/master/topics/sentinel.md