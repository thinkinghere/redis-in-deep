from collections import OrderedDict

# Python OrderedDict 是双向链表+字典
# 实现功能：
# 头部的元素是最新添加/最近使用的 尾部的元素在容量不够的情况下首先被删除

"""
参考：https://www.liaoxuefeng.com/wiki/1016959663602400/1017681679479008#0
"""
class LRUDict(OrderedDict):

    def __init__(self, capacity):
        super(LRUDict, self).__init__()
        self.capacity = capacity
        self.items = OrderedDict()

    def __setitem__(self, key, value):
        old_value = self.items.get(key)
        if old_value is not None:
            self.items.pop(key)  # 先删除key
            self.items[key] = value
            print('old_value')
        elif len(self.items) < self.capacity:  # 容量
            # print('self.items: ', self.items)
            # print('self.capacity: ', self.capacity)
            self.items[key] = value
        else:
            print('self.items in else: ', self.items)  # 字典的赋值会先执行
            res = self.items.popitem(last=False)  # last=True是 后进先出LIFO 栈结构 last=False是队列结构 先进先出
            # print('res: ', res)
            self.items[key] = value

    def __getitem__(self, key):
        value = self.items.get(key)
        if value is not None:
            self.items.pop(key)
            self.items[key] = value
        return value

    def __repr__(self):
        return repr(self.items)


def capacity_test():
    # 超出容量测试
    d = LRUDict(10)
    for i in range(15):
        d[i] = i
    print(d)

if __name__ == "__main":
    # capacity_test()
