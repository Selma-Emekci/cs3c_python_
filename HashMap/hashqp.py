"""
CS3C, HashQP
Copyright 2021 Zibin Yang
Modified by Selma Emekci
"""

from enum import Enum
from prime import *
import math
import copy
import random


class Bucket:
    class State(Enum):
        ACTIVE = 0
        EMPTY = 1
        DELETED = 2

    __slots__ = ("_data", "_state")

    def __init__(self, data=None):
        self._data = data
        self._state = Bucket.State.EMPTY

    def __repr__(self):
        if self._state == Bucket.State.EMPTY:
            return "<State.EMPTY>"
        if self._state == Bucket.State.DELETED:
            return "<State.DELETED>"
        return repr(self._data)


class HashQP:
    INIT_TABLE_SIZE = 97
    INIT_MAX_LAMBDA = 0.49

    class DuplicateDataError(ValueError):
        pass

    def __init__(self, table_size=None):
        if table_size is None or table_size < HashQP.INIT_TABLE_SIZE:
            self._table_size = self._next_prime(HashQP.INIT_TABLE_SIZE)
        else:
            self._table_size = self._next_prime(table_size)

        self._buckets = [Bucket() for _ in range(self._table_size)]
        self._max_lambda = HashQP.INIT_MAX_LAMBDA
        self._nitems = 0
        self._noccupied = 0
        self._ncollisions = 0

    @property
    def nitems(self):
        return self._nitems

    @property
    def noccupied(self):
        return self._noccupied

    @property
    def nbuckets(self):
        return self._table_size

    @property
    def max_lambda(self):
        return self._max_lambda

    def __repr__(self):
        return (
            f"HashQP: nitems={self._nitems}, noccupied={self._noccupied}, "
            f"nbuckets={self._table_size}, max_lambda={self._max_lambda}, "
            f"ncollisions={self._ncollisions}"
        )
    def _internal_hash(self, item):
        return hash(item) % self._table_size

    def _next_prime(self, floor):
        if floor <= 2:
            return 2
        if floor == 3:
            return 3
        candidate = floor + 1 if floor % 2 == 0 else floor
        while True:
            if candidate % 3 != 0:
                limit = int((math.sqrt(candidate) + 1) / 6)
                for k in range(1, limit + 1):
                    if candidate % (6 * k - 1) == 0:
                        break
                    if candidate % (6 * k + 1) == 0:
                        break
                    if k == limit:
                        return candidate
            candidate += 2

    def _iter_index(self, key):
        start = self._internal_hash(key)
        yield start
        step = 1
        idx = start
        while True:
            idx += step
            step += 2
            if idx >= self._table_size:
                idx -= self._table_size
            yield idx

    def _rehash_if_needed(self):
        if self._noccupied > self._max_lambda * self._table_size:
            self._rehash()

    def _rehash(self):
        old_buckets = self._buckets
        old_size = self._table_size
        self._table_size = self._next_prime(2 * old_size)
        self._buckets = [Bucket() for _ in range(self._table_size)]
        self._nitems = 0
        self._noccupied = 0
        self._ncollisions = 0

        for b in old_buckets:
            if b._state == Bucket.State.ACTIVE:
                self.insert(b._data)
    def insert(self, item):
        """Insert unique item; return True if inserted; raise if duplicate."""
        first_empty_idx = None

        for idx in self._iter_index(item):
            bucket = self._buckets[idx]
            st = bucket._state

            if st == Bucket.State.ACTIVE:
                # collision path
                self._ncollisions += 1
                if bucket._data == item:
                    raise ValueError("Duplicate insert")
                continue

            if st == Bucket.State.EMPTY:
                target = idx
                if first_empty_idx is None:
                    first_empty_idx = idx
                target = first_empty_idx
                self._buckets[target]._data = item
                self._buckets[target]._state = Bucket.State.ACTIVE
                self._nitems += 1
                self._noccupied += 1
                self._rehash_if_needed()
                return True
            self._ncollisions += 1
            continue

    def __contains__(self, key):
        for idx in self._iter_index(key):
            bucket = self._buckets[idx]
            st = bucket._state
            if st == Bucket.State.ACTIVE and bucket._data == key:
                return True
            if st == Bucket.State.EMPTY:
                return False
        return False

    def remove(self, key):
        for idx in self._iter_index(key):
            bucket = self._buckets[idx]
            st = bucket._state
            if st == Bucket.State.ACTIVE and bucket._data == key:
                bucket._state = Bucket.State.DELETED
                self._nitems -= 1
                return True
            if st == Bucket.State.EMPTY:
                return False
        return False
    # --- NEW: required by Assignment 7 ---

    def find(self, key):
        """
        Return the stored item x such that x == key, or raise KeyError.
        Works whether 'key' is the same type as stored items or just
        a key that compares equal to them (e.g. our HashMap _Entry vs. bare key).
        Average-case O(1).
        """
        bucket = self._find_pos(key)
        cell = self._buckets[bucket]
        if cell._state == self.HashEntry.State.ACTIVE and cell._data == key:
            return cell._data
        raise KeyError(key)

    def __iter__(self):
        """
        Iterate over ACTIVE items in the table. Average-case O(n).
        """
        for cell in self._buckets:
            if cell._state == self.HashEntry.State.ACTIVE:
                yield cell._data

    def __eq__(self, other):
        """
        Equality by set-of-items: same type and same ACTIVE contents.
        Average-case O(n).
        """
        if not isinstance(other, HashQP):
            return False
        if self._size != other._size:
            return False
        # Verify each of our items exists in 'other'
        for x in self:
            if x not in other:
                return False
        # And vice-versa (sizes match, so this is symmetric but keep explicit)
        for y in other:
            if y not in self:
                return False
        return True


    def debug_dump(self):
        print("hashtable is:")
        print(self)
        print("buckets=[{}]".format(", ".join(repr(b) for b in self._buckets)))
