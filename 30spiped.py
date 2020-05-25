import redis
c = redis.StrictRedis(host="localhost", port=6579)
print(c.ping())
print(c.info('cpu'))


# 使用spiped
# brew install spiped
# yum install spiped
# 使用 Docker 启动 redis-server，注意要绑定本机的回环127.0.0.1；
"""
生成随机的密钥文件；
dd if=/dev/urandom bs=32 count=1 of=spiped.key

172.18.0.154 是本机公网IP
➜  ~ spiped -d -s '[172.18.0.154]:6479' -t '[127.0.0.1]:6385' -k ~/Downloads/spiped.key
➜  ~ ps -ef|grep spiped
  501 95390     1   0  3:10下午 ??         0:00.00 spiped -d -s [172.18.0.154]:6479 -t [127.0.0.1]:6385 -k /Users/mac/Downloads/spiped.key
  501 95412  4212   0  3:10下午 ttys002    0:00.00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox spiped
➜  ~ spiped -e -s '[127.0.0.1]:6579' -t '[172.18.0.154]:6479' -k spiped.key
spiped: Cannot open file: spiped.key: No such file or directory
spiped: Error reading shared secret
➜  ~ spiped -e -s '[127.0.0.1]:6579' -t '[172.18.0.154]:6479' -k ~/Downloads/spiped.key
➜  ~ ps -ef|grep spiped
  501 95390     1   0  3:10下午 ??         0:00.00 spiped -d -s [172.18.0.154]:6479 -t [127.0.0.1]:6385 -k /Users/mac/Downloads/spiped.key
  501 95708     1   0  3:11下午 ??         0:00.00 spiped -e -s [127.0.0.1]:6579 -t [172.18.0.154]:6479 -k /Users/mac/Downloads/spiped.key
  501 95722  4212   0  3:11下午 ttys002    0:00.00 grep --color=auto --exclude-dir=.bzr --exclude-dir=CVS --exclude-dir=.git --exclude-dir=.hg --exclude-dir=.svn --exclude-dir=.idea --exclude-dir=.tox spiped
➜  ~
"""
