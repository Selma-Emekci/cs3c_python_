"""
CS3C, HashQP test
Copyright 2022 Zibin Yang
Modified Selma Emekci
"""
from hashqp import *
from hashtable_test import *
import unittest
import random

class HashQPNewMethodsTest(unittest.TestCase):
    def test_find_hits_and_misses(self):
        h = HashQP(97)
        data = [53, 274, 89, 787, 417, 272, 110, 858, 922, 895]
        for x in data:
            self.assertTrue(h.insert(x))
        for x in data:
            self.assertEqual(h.find(x), x)
        for x in (9999, -1, 123456):
            with self.assertRaises(KeyError):
                _ = h.find(x)

    def test_iter_yields_active_items(self):
        h = HashQP(11)
        keep = [2, 4, 6, 8, 10]
        for x in keep:
            h.insert(x)
        h.remove(6)

        seen = list(h)
        self.assertEqual(sorted(seen), sorted([2, 4, 8, 10]))

    def test_eq_same_items_different_order(self):
        a = HashQP(97)
        b = HashQP(97)

        left = [1, 3, 5, 7, 9, 11]
        right = [11, 9, 7, 5, 3, 1]

        for x in left:
            a.insert(x)
        for x in right:
            b.insert(x)

        self.assertTrue(a == b)

        b.remove(7)
        b.insert(8)
        self.assertFalse(a == b)
        self.assertFalse(a == 123)


if __name__ == "__main__":
    unittest.main()
