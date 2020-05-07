from rediscluster import RedisCluster

# Requires at least one node for cluster discovery. Multiple nodes is recommended.

startup_nodes = [{"host": "127.0.0.1", "port": "7000"}]

# Note: See note on Python 3 for decode_responses behaviour
rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)

# rc.set("foo", "bar")

print(rc.get("foo"))
