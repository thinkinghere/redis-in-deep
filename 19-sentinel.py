from redis.sentinel import Sentinel
sentinel = Sentinel([('172.18.0.98', 26379)], socket_timeout=0.1)
print(sentinel)
mymaster = sentinel.discover_master('mymaster')
""""
redis.exceptions.ResponseError: DENIED Redis is running in protected mode because protected mode is enabled, no bind address was specified, no authentication 
password is requested to clients. In this mode connections are only accepted from the loopback interface. If you want to connect from external computers to Re
dis you may adopt one of the following solutions: 1) Just disable protected mode sending the command 'CONFIG SET protected-mode no' from the loopback interfac
e by connecting to Redis from the same host the server is running, however MAKE SURE Redis is not publicly accessible from internet if you do so. Use CONFIG R
EWRITE to make this change permanent. 2) Alternatively you can just disable the protected mode by editing the Redis configuration file, and setting the protec
ted mode option to 'no', and then restarting the server. 3) If you started the server manually just for testing, restart it with the '--protected-mode no' opt
ion. 4) Setup a bind address or an authentication password. NOTE: You only need to do one of the above things in order for the server to start accepting connections from the outside
"""
print(mymaster)
# ('127.0.0.1', 6379)
# sentinel.discover_slaves('mymaster')
# [('127.0.0.1', 6380)]
master = sentinel.master_for('mymaster', socket_timeout=0.1)
slave = sentinel.slave_for('mymaster', socket_timeout=0.1)
master.set('foo', 'bar')
slave.get('foo')
