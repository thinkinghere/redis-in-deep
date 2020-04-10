# coding: utf8

import time


class Funnel(object):
    def __init__(self, capacity, leaking_rate):
        self.capacity = capacity  # 漏斗容量
        self.leaking_rate = leaking_rate  # 漏嘴流水速率
        self.left_quota = capacity  # 漏斗剩余空间
        self.leaking_ts = time.time()  # 上一次漏水时间

    def make_space(self):
        now_ts = time.time()
        delta_ts = now_ts - self.leaking_ts  # 距离上一次漏水过去了多久
        delta_quota = delta_ts * self.leaking_rate  # 又可以腾出不少空间了
        if delta_quota < 1:
            # 腾的空间太少，那就等下次吧
            return
        self.left_quota += delta_quota  # 增加剩余空间
        self.leaking_ts = now_ts  # 记录漏水时间
        if self.left_quota > self.capacity:
            # 剩余空间不得高于容量
            self.left_quota = self.capacity

    def watering(self, quota):
        self.make_space()
        if self.left_quota >= quota:
            # 判断剩余空间是否足够
            self.left_quota -= quota  # 每次调用会将容量-1
            return True
        return False


funnels = {}  # 所有的漏斗

# capacity 漏斗容量
# leaking_rate 漏嘴流水速率 quota/s


def is_action_allowed(user_id, action_key, capacity, leaking_rate):
    key = '%s:%s' % (user_id, action_key)
    funnel = funnels.get(key)
    if not funnel:
        funnel = Funnel(capacity, leaking_rate)
        funnels[key] = funnel
    return funnel.watering(1)


if __name__ == '__main__':
    for i in range(20):
        print(is_action_allowed('user01', 'reply', 15, 0.5))
