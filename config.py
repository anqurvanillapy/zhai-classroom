"""Server config loader
"""

import json
import datetime as dt

CFG_NAME = ".apprc"


def read():
    _cfg = {
        "timedelta": dt.timedelta(weeks=1),
        "img_path": "img",
        "max_filename_length": 128,
        "max_content_length": 5 * 1024 * 1024,
        "allowed_fileexts": ["png", "jpg", "jpeg"],
    }

    with open(CFG_NAME, "r") as f:
        _cfg.update(json.loads(f.read()))
        return _cfg
