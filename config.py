"""Server config loader
"""

import json
import datetime as dt

CFG_NAME = ".zhairc"


def read():
    # Public.
    _cfg = {"timedelta": dt.timedelta(weeks=1)}

    # Private.
    with open(CFG_NAME, "r") as f:
        _cfg.update(json.loads(f.read()))
        return _cfg
