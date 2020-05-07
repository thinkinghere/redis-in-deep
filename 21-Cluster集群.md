进入源码包的的redis-5.0.8/utils/create-cluster

### start

./create-cluster start

```
[root@k8s-master create-cluster]# ./create-cluster start
Starting 30001
Starting 30002
Starting 30003
Starting 30004
Starting 30005
Starting 30006
```

### create

启动了5个进程

```
[root@k8s-master create-cluster]# ps -ef |grep redis
redis     81010      1  0 04:01 ?        00:00:00 /usr/bin/redis-server 0.0.0.0:6379
root      91025      1  0 04:08 ?        00:00:00 ../../src/redis-server *:30001 [cluster]
root      91027      1  0 04:08 ?        00:00:00 ../../src/redis-server *:30002 [cluster]
root      91029      1  0 04:08 ?        00:00:00 ../../src/redis-server *:30003 [cluster]
root      91031      1  0 04:08 ?        00:00:00 ../../src/redis-server *:30004 [cluster]
root      91033      1  0 04:08 ?        00:00:00 ../../src/redis-server *:30005 [cluster]
root      91035      1  0 04:08 ?        00:00:00 ../../src/redis-server *:30006 [cluster]
root      91708  11563  0 04:09 pts/0    00:00:00 grep --color=auto redis
```


./create-cluster create

最后一定是要输入 yes, 生成16384个槽

```
[root@k8s-master create-cluster]# ./create-cluster start
Starting 30001
Starting 30002
Starting 30003
Starting 30004
Starting 30005
Starting 30006
[root@k8s-master create-cluster]# ./create-cluster create
>>> Performing hash slots allocation on 6 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
Adding replica 127.0.0.1:30005 to 127.0.0.1:30001
Adding replica 127.0.0.1:30006 to 127.0.0.1:30002
Adding replica 127.0.0.1:30004 to 127.0.0.1:30003
>>> Trying to optimize slaves allocation for anti-affinity
[WARNING] Some slaves are in the same host as their master
M: c0f18857b7d2bc6ae0ac0475de9a6308df046fed 127.0.0.1:30001
   slots:[0-5460] (5461 slots) master
M: 3cd9bc18553bc49a76e41b1a946239c59a599219 127.0.0.1:30002
   slots:[5461-10922] (5462 slots) master
M: 3997fad9c9b1f2d85187d8a8b5665b9e7753a3d1 127.0.0.1:30003
   slots:[10923-16383] (5461 slots) master
S: cf40bd8ddedeba51a607eff4df5aac406c9f88ae 127.0.0.1:30004
   replicates 3cd9bc18553bc49a76e41b1a946239c59a599219
S: 501b16f3ee0af61992db82034e3cea4614edc66c 127.0.0.1:30005
   replicates 3997fad9c9b1f2d85187d8a8b5665b9e7753a3d1
S: b19e04bdf6bebe2c5e76198996d235431a773ace 127.0.0.1:30006
   replicates c0f18857b7d2bc6ae0ac0475de9a6308df046fed
Can I set the above configuration? (type 'yes' to accept): yes
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
..
>>> Performing Cluster Check (using node 127.0.0.1:30001)
M: c0f18857b7d2bc6ae0ac0475de9a6308df046fed 127.0.0.1:30001
   slots:[0-5460] (5461 slots) master
   1 additional replica(s)
M: 3cd9bc18553bc49a76e41b1a946239c59a599219 127.0.0.1:30002
   slots:[5461-10922] (5462 slots) master
   1 additional replica(s)
M: 3997fad9c9b1f2d85187d8a8b5665b9e7753a3d1 127.0.0.1:30003
   slots:[10923-16383] (5461 slots) master
   1 additional replica(s)
S: cf40bd8ddedeba51a607eff4df5aac406c9f88ae 127.0.0.1:30004
   slots: (0 slots) slave
   replicates 3cd9bc18553bc49a76e41b1a946239c59a599219
S: b19e04bdf6bebe2c5e76198996d235431a773ace 127.0.0.1:30006
   slots: (0 slots) slave
   replicates c0f18857b7d2bc6ae0ac0475de9a6308df046fed
S: 501b16f3ee0af61992db82034e3cea4614edc66c 127.0.0.1:30005
   slots: (0 slots) slave
   replicates 3997fad9c9b1f2d85187d8a8b5665b9e7753a3d1
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.
```


#### 查看集群结点信息



redis-cli -c -p 30001
```
-c表示以集群方式连接redis，

-h指定ip地址，

-p指定端口号
```

查询集群结点信息
```
127.0.0.1:30001> cluster nodes
3cd9bc18553bc49a76e41b1a946239c59a599219 127.0.0.1:30002@40002 master - 0 1588843593542 2 connected 5461-10922
3997fad9c9b1f2d85187d8a8b5665b9e7753a3d1 127.0.0.1:30003@40003 master - 0 1588843593142 3 connected 10923-16383
c0f18857b7d2bc6ae0ac0475de9a6308df046fed 127.0.0.1:30001@40001 myself,master - 0 1588843593000 1 connected 0-5460
cf40bd8ddedeba51a607eff4df5aac406c9f88ae 127.0.0.1:30004@40004 slave 3cd9bc18553bc49a76e41b1a946239c59a599219 0 1588843593643 4 connected
b19e04bdf6bebe2c5e76198996d235431a773ace 127.0.0.1:30006@40006 slave c0f18857b7d2bc6ae0ac0475de9a6308df046fed 0 1588843593042 6 connected
501b16f3ee0af61992db82034e3cea4614edc66c 127.0.0.1:30005@40005 slave 3997fad9c9b1f2d85187d8a8b5665b9e7753a3d1 0 1588843593142 5 connected
```

查询集群状态
```
127.0.0.1:30001> cluster info
cluster_state:ok
cluster_slots_assigned:16384
cluster_slots_ok:16384
cluster_slots_pfail:0
cluster_slots_fail:0
cluster_known_nodes:6
cluster_size:3
cluster_current_epoch:6
cluster_my_epoch:1
cluster_stats_messages_ping_sent:5484
cluster_stats_messages_pong_sent:5455
cluster_stats_messages_sent:10939
cluster_stats_messages_ping_received:5450
cluster_stats_messages_pong_received:5484
cluster_stats_messages_meet_received:5
cluster_stats_messages_received:10939
```

## 使用集群

需要加上参数-c
redis-cli -c -p

```
[root@k8s-master create-cluster]# redis-cli -c -p 30001
127.0.0.1:30001> set foo bar
-> Redirected to slot [12182] located at 127.0.0.1:30003
OK
```


### Django Redis Cluster configuration

```py
"default": {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION':"redis://mycluster.foo.clustercfg.use1.cache.amazonaws.com/0",
    'OPTIONS': {
        'REDIS_CLIENT_CLASS': 'rediscluster.StrictRedisCluster',
        'CONNECTION_POOL_CLASS': 'rediscluster.connection.ClusterConnectionPool',
        'CONNECTION_POOL_KWARGS': {
            'skip_full_coverage_check': True  # AWS ElasticCache has disabled CONFIG commands
         }
    }
```

ref:
https://www.imooc.com/article/67005

https://blog.csdn.net/weixin_30457881/article/details/95603864?utm_medium=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-BlogCommendFromBaidu-2

https://redis-py-cluster.readthedocs.io/en/master/

https://www.cnblogs.com/cqming/p/11191079.html