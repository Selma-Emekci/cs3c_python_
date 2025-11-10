"""
CS3C, Generic HashTable tests
Copyright 2022 Zibin Yang
"""
import unittest
import random


class HashTableTestCase(unittest.TestCase):
    HashTableType = None

    def setUp(self):
        # Use to same seed to have reproducible data sequence for each test.
        random.seed(123)

    def helpTestInsert(self, all_data, test_data, expected, hashtable):
        for d in test_data:
            expected.add(d)
            hashtable.insert(d)
            self.assertEqual(len(expected), len(hashtable))
            for i in all_data:
                self.assertEqual(i in expected, i in hashtable)

    def testRemove1(self):
        self.helpTestCompleteRemove(1000, 10, 15)

    def testRemove2(self):
        self.helpTestCompleteRemove(1000, 100, 150)

    @unittest.skip("This takes a while to run")
    def testRemove3(self):
        self.helpTestCompleteRemove(5000, 1000, 1500)

    def helpTestRemove(self, all_data, test_data, expected, hashtable):
        for i in all_data:
            try:
                expected.remove(i)
                # Removed
                hashtable.remove(i)
                self.assertEqual(len(expected), len(hashtable))
                self.assertFalse(i in hashtable)
            except KeyError:
                with self.assertRaises(KeyError):
                    hashtable.remove(i)

    def helpTestCompleteRemove(self, max_, size1, size2):
        all_data = range(max_)
        test_data1 = random.sample(all_data, size1)
        print("test_data1", test_data1)

        expected = set()
        hashtable = self.HashTableType(2)

        print("initial insert")
        self.helpTestInsert(all_data, test_data1, expected, hashtable)

        print("re-insert same data, should get ValueError")
        for d in test_data1:
            with self.assertRaises(ValueError):
                hashtable.insert(d)

        # Test simple remove
        print("initial remove")
        self.helpTestRemove(all_data, test_data1, expected, hashtable)

        # Reinsert same data after remove
        print("re-insert same data")
        self.helpTestInsert(all_data, test_data1, expected, hashtable)

        # Remove all of them again
        print("re-remove same data")
        self.helpTestRemove(all_data, test_data1, expected, hashtable)

        # Insert a different set of data
        test_data2 = random.sample(all_data, size2)
        print("test_data2", test_data2)
        print("insert test_data2")
        self.helpTestInsert(all_data, test_data2, expected, hashtable)

        print(hashtable)

    def testRepr(self):
        hashtable = self.HashTableType(2)
        data = random.sample(range(100), 5)
        for d in data:
            hashtable.insert(d)
        print(f"hashtable is:\n{repr(hashtable)}")

    # New 5/17/2022: some tests specifically for probing table's DELETED buckets
    def oldTestCannotUseNitemsToCalculateLambda(self):
        """This shows HashQP cannot use .nitems for calculating lambda"""
        # This is an old, more complex way of showing it; the one below is
        # simpler.
        all_data = range(1000)
        test_data = random.sample(all_data, 10)
        # print(test_data)

        expected = set()
        hashtable = self.HashTableType(2)

        for d in test_data:
            # Insert data, check __contains__().
            expected.add(d)
            hashtable.insert(d)
            print(f"\nAdded {d=}")
            self.assertEqual(len(expected), len(hashtable))
            for i in all_data:
                # print(f"\nAsserting {i} is in hashtable")
                self.assertEqual(i in expected, i in hashtable)
            # Remove data right away, check __contains__().
            # This exposes the bug in HashQP._rehash_as_needed() that used
            # self._nitems to calculate the load factor.  It should use
            # self._noccupied.
            expected.remove(d)
            hashtable.remove(d)
            print(f"\nRemoved {d=}")
            for i in all_data:
                # print(f"\nAsserting {i} is not in hashtable")
                self.assertEqual(i in expected, i in hashtable)

        print(hashtable)

    def testCannotUseNitemsToCalculateLambda(self):
        """This shows HashQP cannot use .nitems for calculating lambda"""
        hashtable = self.HashTableType(5)
        hashtable.insert(0)
        hashtable.insert(1)
        hashtable.remove(0)
        hashtable.remove(1)
        # We now have 2 DELETED buckets.

        # Insert another number that hashed to bucket 0; this should expand
        # the number of buckets; but if HashQP uses .nitems to calculate
        # lambda, there's only one active bucket, so it won't expand...
        hashtable.insert(10)
        # ... in which case inserting 20 would try to find an empty bucket
        # in 2 remaining empty bucket out of 5, and fail to do so.
        hashtable.insert(20)

    def testCannotReuseDeletedBucket(self):
        """This shows HashQP cannot reuse DELETED bucket for insertion"""
        hashqp = self.HashTableType(7)
        hashqp.insert(7)
        hashqp.insert(14)
        hashqp.remove(7)
        with self.assertRaises(ValueError):
            # This should detect the duplicate. But if HashQP inserts 14
            # into the DELETED 7 bucket, it won't see the existing 14 later
            # in the probing sequence.
            hashqp.insert(14)

    def testCannotStopAtDeletedBucketWithSameData(self):
        """This shows HashQP cannot stop at DELETED bucket w/ same data in search"""
        hashqp = self.HashTableType(7)
        hashqp.insert(7)
        hashqp.remove(7)
        hashqp.insert(7)
        # This should see 7 in the hash table. But if HashQP doesn't reuse
        # DELETED bucket even for the same item, then it can have duplicate
        # 7 in multiple buckets, and the probing might see the DELETED 7
        # first, and if it stops there, then it'll incorrectly say 7 is not
        # in the table.
        self.assertTrue(7 in hashqp)
