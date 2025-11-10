"""
CS3C, Assignment #7, Implementing HashMap
Selma Emekci
A dict-like HashMap implemented on top of HashQP.
"""

from hashqp import HashQP
"""
CS3C, Assignment #7, Implementing HashMap
Your Name
"""

from hashqp import HashQP


class _Entry:
    """
    Internal key/value wrapper stored in HashQP.
    - __hash__ / __eq__ are based on key only so probing is by key.
    - Equality vs. a bare key is allowed so HashQP.find(key) works.
    """
    __slots__ = ("key", "value")

    def __init__(self, key, value):
        self.key = key
        self.value = value

    def __hash__(self):
        return hash(self.key)

    def __eq__(self, other):
        if isinstance(other, _Entry):
            return self.key == other.key
        return self.key == other  # allow compare to bare key

    def __repr__(self):
        return f"_Entry({self.key!r}, {self.value!r})"


class HashMap:
    """
    Minimal dict-like map built on top of HashQP.
    Average-case O(1) for insert and lookup.
    """

    def __init__(self):
        self._table = HashQP()
        self._size = 0

    def __len__(self):
        return self._size

    def __getitem__(self, key):
        entry = self._table.find(key)  # returns stored _Entry
        return entry.value

    def __setitem__(self, key, value):
        try:
            entry = self._table.find(key)  # update existing
            entry.value = value
        except KeyError:
            # new key
            self._table.insert(_Entry(key, value))
            self._size += 1

    def __iter__(self):
        # iterate over keys (dict semantics)
        for entry in self._table:
            yield entry.key

    def __eq__(self, other):
        if not isinstance(other, HashMap):
            return False
        if len(self) != len(other):
            return False
        # verify same key->value pairs
        for entry in self._table:
            try:
                if other[entry.key] != entry.value:
                    return False
            except KeyError:
                return False
        return True

    # Optional conveniences (not required but handy)
    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def keys(self):
        return iter(self)

    def values(self):
        for entry in self._table:
            yield entry.value

    def items(self):
        for entry in self._table:
            yield (entry.key, entry.value)
