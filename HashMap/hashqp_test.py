"""
CS3C, HashQP test
Copyright 2022 Zibin Yang
Modified by Selma Emekci
"""
from hashqp import *
from hashtable_test import *


class HashQPTestCase(HashTableTestCase):
    HashTableType = HashQP
    def testIterIndex(self):
        hashqb = HashQP()
        key = 7
        k = 0
        simple_generator = hashqb._iter_index_slow(key)
        optimized_generator = hashqb._iter_index(key)
        while k < 50:
            simple = next(simple_generator)
            optimized = next(optimized_generator)
            self.assertEqual(simple, optimized, f"k is {k}")
            k += 1

    # New 5/17/2022: some tests specifically for probing table's DELETED buckets
    def testCannotUseNitemsToCalculateLambda(self):
        """This shows HashQP cannot use .nitems for calculating lambda"""
        super().testCannotUseNitemsToCalculateLambda()

    def testCannotReuseDeletedBucket(self):
        """This shows HashQP cannot reuse DELETED bucket for insertion"""
        super().testCannotReuseDeletedBucket()

    def testCannotStopAtDeletedBucketWithSameData(self):
        """This shows HashQP cannot stop at DELETED bucket w/ same data in search"""
        super().testCannotStopAtDeletedBucketWithSameData()

    def testCollisions(self):
        """This shows collision count (assuming HashTableType implements it)"""
        hashtable = self.HashTableType(2)
        nsamples = 500
        max_ = nsamples * 2
        list_of_data = random.sample(range(max_), nsamples)
        for data in list_of_data:
            hashtable.insert(data)
        print(f"{hashtable}")

class HashQPNewMethodsTest(unittest.TestCase):
    def test_find_hits_and_misses(self):
        h = HashQP()
        data = random.sample(range(10000), 200)
        for x in data:
            self.assertTrue(h.insert(x))
        for x in data[:20]:
            self.assertEqual(h.find(x), x)
        for y in [10001, 10002, -5, 123456789]:
            with self.assertRaises(KeyError):
                _ = h.find(y)

    def test_iter_yields_active_only(self):
        h = HashQP()
        keep = set()
        toss = set()
        for x in range(100, 150):
            h.insert(x)
            keep.add(x)
        for x in range(200, 230):
            h.insert(x)
            toss.add(x)
        for x in list(toss)[:10]:
            h.remove(x)

        seen = set(h)
        self.assertTrue(keep.issubset(seen))
        self.assertFalse(any(x in seen for x in list(toss)[:10]))

    def test_eq_same_items_different_layouts(self):
        a = HashQP()
        b = HashQP()
        items = list(range(300))
        random.shuffle(items)
        for x in items:
            a.insert(x)
        for x in reversed(items):
            b.insert(x)
        self.assertTrue(a == b)
        self.assertTrue(a.remove(items[0]))
        self.assertFalse(a == b)

    def test_insert_duplicate_raises(self):
        h = HashQP()
        self.assertTrue(h.insert(42))
        with self.assertRaises(ValueError):
            h.insert(42)

    def test_remove_then_find_raises(self):
        h = HashQP()
        h.insert("abc")
        self.assertTrue("abc" in h)
        self.assertTrue(h.remove("abc"))
        self.assertFalse("abc" in h)
        with self.assertRaises(KeyError):
            h.find("abc")

if __name__ == "__main__":
    unittest.main()

del HashTableTestCase
