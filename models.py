"""Data models.
"""


class Dogs:

    def __init__(self):
        self._store = {}

    def __getitem__(self, k):
        return self._store.get(k)

    def __setitem__(self, k, v):
        self._store[k] = v

    def __delitem__(self, k):
        del self._store[k]
