"""Data models.
"""

# 狗子数据库, 还没有使用 MySQL, 先用内存存储的 dict 代替.
class Dogs:

    def __init__(self, pre=[]):
        # 狗子是从 用户名 到 密码 的一个映射 (map).
        self._store = {}
        try:
            # 尝试把提前要存的狗子 (pre) 存入, 比如用作测试.
            self._store.update(pre)
        except:
            # 发生错误不用处理.
            pass

    def __getitem__(self, k):
        # 根据用户名获取狗子的密码.
        return self._store.get(k)

    def __setitem__(self, k, v):
        # 修改用户名对应的密码.
        self._store[k] = v

    def __delitem__(self, k):
        # 删除某个用户.
        del self._store[k]
