import redlock

addrs = [{
    "host": "localhost",
    "port": 6379,
    "db": 0
}, {
    "host": "localhost",
    "port": 6380,
    "db": 0
}, {
    "host": "localhost",
    "port": 6382,
    "db": 0
}]

dlm = redlock.Redlock(addrs)
success = dlm.lock("user-lck-aaa", 5000)

if success:
    print('lock success')
    dlm.unlock('user-lck-laoqian')
else:
    print('lock failed')
