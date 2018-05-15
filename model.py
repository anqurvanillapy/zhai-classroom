"""Data models.
"""


class Students:

    def __init__(self, *pre):
        self._store = {}
        self._item = {
            "username": None,
            "is_admin": False,
            "password": None,
            "name": None,
            "address": None,
            "contact": None,
        }
        if pre:
            try:
                for p in pre:
                    self.__setitem__(p["username"], p)
            except:
                pass

    def __getitem__(self, k):
        return self._store.get(k)

    def getall(self):
        return self._store.values()

    def __setitem__(self, k, v):
        item = self._item.copy()
        item.update(v)
        try:
            self._store[k].update(item)
        except KeyError:
            self._store[k] = item

    def __delitem__(self, k):
        del self._store[k]


class Bulletins:

    def __init__(self, *pre):
        self._store = []
        self._item = {"title": None, "content": None, "date": None}
        if pre:
            try:
                for p in pre:
                    self.setitem(p)
            except:
                pass

    def getitem(self, i):
        return self._store[i]

    def getall(self):
        return self._store

    def setitem(self, v):
        item = self._item.copy()
        item.update(v)
        self._store.append(item)

    def delitem(self, i):
        del self._store[i]


class Photos:

    def __init__(self, *pre):
        self._store = []
        self._item = {"filename": None, "date": None}
        if pre:
            try:
                for p in pre:
                    self.setitem(p)
            except:
                pass

    def getitem(self, i):
        return self._store[i]

    def getall(self):
        return self._store

    def setitem(self, v):
        item = self._item.copy()
        item.update(v)
        self._store.append(item)

    def delitem(self, i):
        del self._store[i]
