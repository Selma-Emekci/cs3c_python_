"""
CS3C, HashSC tests
Copyright 2021 Zibin Yang
"""
from hashsc import *
from hashtable_test import *


class HashSCTestCase(HashTableTestCase):
    HashTableType = HashSC

    def testHashSCInsert(self):
        # Intrusive test that assume certain implementation
        hashsc = HashSC(2)
        self.assertEqual(2, len(hashsc._buckets))
        self.assertEqual(0, len(hashsc))

        key = 10
        hashsc.insert(key)
        self.assertIsNotNone(hashsc._buckets[0])
        self.assertTrue(key in hashsc._buckets[0])
        self.assertEqual(1, len(hashsc))

    def testHashSCRehash(self):
        # Intrusive test that assume certain implementation
        hashsc = HashSC(2)
        data = [1, 3, 5]
        for d in data:
            hashsc.insert(d)

        self.assertEqual(3, len(hashsc))
        expected_nbuckets = 5
        self.assertEqual(expected_nbuckets, len(hashsc._buckets))
        for d in data:
            bucket_index = hash(d) % expected_nbuckets
            self.assertIsNotNone(hashsc._buckets[bucket_index])
            self.assertTrue(d in hashsc._buckets[bucket_index])

    def testHashSCRemove(self):
        hashsc = HashSC(2)
        with self.assertRaises(KeyError):
            hashsc.remove("not there")
        key = 10
        hashsc.insert(key)
        hashsc.remove(key)
        self.assertFalse(key in hashsc)

    # Have to define one test if we only want to run one test
    # def testInsertAndContains(self):
    #     super().testInsertAndContains()

del HashTableTestCase
