"""
CS3C Min heap implementation test
Copyright 2021 Zibin Yang
"""

import unittest
from minheap import *


class MinHeapTestCase(unittest.TestCase):
    def testInsert(self):
        minheap = MinHeap()
        data = [5, 9, 3, 7, 1]
        for d in data:
            minheap.insert(d)

        expected = [None, 1, 3, 5, 9, 7]
        self.assertListEqual(expected, minheap._heap)
        self.assertEqual(len(minheap), len(data))

    def testRemove(self):
        minheap = MinHeap()
        data = [5, 7, 3, 9, 1, 12, 8]
        for d in data:
            minheap.insert(d)

        size = len(data)
        for expected in sorted(data):
            self.assertEqual(expected, minheap.remove())
            size -= 1
            self.assertEqual(size, len(minheap))

        with self.assertRaises(IndexError):
            minheap.remove()

    def testInitWithData1(self):
        data = [5, 9, 3, 7, 1, 12, 8]
        minheap = MinHeap(data)
        expected = [None, 1, 5, 3, 7, 9, 12, 8]
        self.assertListEqual(expected, minheap._heap)
        self.assertEqual(len(data), len(minheap))

    def testInitWithData2(self):
        data = [15, 9, 3, 7, 1]
        minheap = MinHeap(data)
        expected = [None, 1, 7, 3, 15, 9]
        self.assertListEqual(expected, minheap._heap)
        self.assertEqual(len(data), len(minheap))

    def testPeekFailure(self):
        minheap = MinHeap()
        with self.assertRaises(IndexError):
            minheap.peek()

    def testPeek(self):
        minheap = MinHeap()
        data = [5, 7, 3, 9, 1, 12, 8]
        inserted_so_far = []
        for d in data:
            minheap.insert(d)
            inserted_so_far.append(d)
            self.assertEqual(min(inserted_so_far), minheap.peek())