"""Server config loader
"""

import json
import datetime as dt

CFG_NAME = ".apprc"


def read():
    _cfg = {
        "timedelta": dt.timedelta(weeks=10),
        "asset_path": "img",
        "max_filename_lenght": 64,
        "allowed_fileexts": ["png", "jpg", "jpeg"],
    }

    with open(CFG_NAME, "r") as f:
        _cfg.update(json.loads(f.read()))
        return _cfg
