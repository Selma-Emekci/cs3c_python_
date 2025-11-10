"""
CS3C, HashSC
Copyright 2021 Zibin Yang
"""

from prime import *
from linkedlist import *


class HashSC:
    INIT_NUM_BUCKETS = 97
    INIT_MAX_LAMBDA = 1.5

    def __init__(self, nbuckets=INIT_NUM_BUCKETS, max_lambda=INIT_MAX_LAMBDA):
        if not is_prime(nbuckets):
            nbuckets = next_prime(nbuckets)
        self._nbuckets = nbuckets

        self._max_lambda = max_lambda
        self.clear()

    def clear(self):
        self._buckets = [LinkedList() for _ in range(self._nbuckets)]
        self._nitems = 0

    @property
    def size(self):
        return self._nitems

    def __len__(self):
        return self._nitems

    @property
    def max_lambda(self):
        return self._max_lambda

    @max_lambda.setter
    def max_lambda(self, max_lambda):
        if max_lambda > 0:
            self._max_lambda = max_lambda
        else:
            raise ValueError(f"Invalid lambda {max_lambda}")

    def __str__(self):
        return f"{self.__class__.__name__}: size={self.size}," \
               f" nbuckets={self._nbuckets}, max_lambda={self.max_lambda}"

    def __repr__(self):
        return (f"{self}\n"
                + "\n".join(f"bucket[{i}]: {bucket}" for i, bucket in enumerate(self._buckets)))

    def _hash(self, key):
        return hash(key) % self._nbuckets

    def insert(self, item):
        bucket_index = self._hash(item)
        if item in self._buckets[bucket_index]:
            raise ValueError(f"{item} already exists")

        self._buckets[bucket_index].add_to_head(item)
        self._nitems += 1
        if self._nitems / self._nbuckets >= self.max_lambda:
            self._rehash()

    def _rehash(self):
        buckets = self._buckets
        self._nbuckets = next_prime(self._nbuckets * 2)
        self.clear()
        for bucket in buckets:
            for item in bucket:
                self.insert(item)

    def __contains__(self, key):
        bucket_index = self._hash(key)
        return key in self._buckets[bucket_index]

    def remove(self, key):
        bucket_index = self._hash(key)
        self._buckets[bucket_index].remove(key)
        self._nitems -= 1
