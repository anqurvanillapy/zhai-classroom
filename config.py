"""Server config loader
"""

import json
import datetime as dt

# 配置文件名.
CFG_NAME = ".zhairc"


def read():
    # 可公开的配置, 比如令牌合法的时间跨度.
    _cfg = {"timedelta": dt.timedelta(seconds=10)}

    # 私有的配置, 在 .zhairc 中, 比如 令牌的秘密.
    with open(CFG_NAME, "r") as f:
        # 从文件中读取出 JSON 格式的数据, 通过 json.loads 转成 dict 格式,
        # 更新到 _cfg 这个对象中.
        _cfg.update(json.loads(f.read()))
        # 返回 _cfg 供 app 使用.
        return _cfg
