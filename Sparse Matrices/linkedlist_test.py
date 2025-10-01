"""
CS3C, LinkedList and OrderedLinkedList tests

Copyright 2022 Zibin Yang
"""
import copy
import unittest
from linkedlist import *


class LinkedListTestCase(unittest.TestCase):
    def testInit(self):
        ll = LinkedList()
        self.assertIsNone(ll._head)
        self.assertEqual(0, ll.size)
        self.assertEqual(0, len(ll))

    # Added 4/5/21: made it easier to initialize the list
    def testInitWithList(self):
        data = [4, 2, 9]
        ll = LinkedList(data)
        self.assertEqual(len(data), len(ll))
        for i in range(len(data)):
            self.assertEqual(data[i], ll[i])

    # Added 4/15/22: test init with data that's unordered (a set)
    def testInitWithSet(self):
        data = {4, 2, 9}
        ll = LinkedList(data)
        self.assertEqual(len(data), len(ll))
        # Set comparison, assuming __iter__() works.
        self.assertEqual(data, {d for d in ll})

    def testAddToHead(self):
        ll = LinkedList()
        ll.add_to_head(10)
        self.assertEqual(10, ll._head.data)
        self.assertIsNone(ll._head.next)
        self.assertEqual(1, len(ll))

        ll.add_to_head(20)
        self.assertEqual(20, ll._head.data)
        self.assertEqual(10, ll._head.next.data)
        self.assertIsNone(ll._head.next.next)
        self.assertEqual(2, len(ll))

    def testIter(self):
        ll = LinkedList()
        ll.add_to_head(10)
        ll.add_to_head(20)
        ll.add_to_head(30)
        expected = [30, 20, 10]
        actual = [d for d in ll]
        self.assertEqual(expected, actual)

    def testStr(self):
        ll = LinkedList()
        ll.add_to_head(10)
        ll.add_to_head(20)
        ll.add_to_head(30)
        self.assertEqual(str, type(ll.__str__()))
        self.assertEqual("30 20 10", ll.__str__())
        print(ll)

    def testFind(self):
        l = [1, 202, 33, 64, 5]
        ll = LinkedList()
        for i in l:
            ll.add_to_head(i)

        for i in l:
            actual = ll.find(i)
            self.assertEqual(i, actual)

    def testFindFailure(self):
        ll = LinkedList()

        with self.assertRaises(KeyError):
            ll.find("no there")

        l = [1, 202, 33, 64, 5]
        ll = LinkedList()
        for i in l:
            ll.add_to_head(i)

        with self.assertRaises(KeyError):
            ll.find(666)

    def testContains(self):
        l = [1, 202, 33, 64, 5]
        ll = LinkedList()
        for i in l:
            ll.add_to_head(i)

        for i in l:
            self.assertTrue(ll.__contains__(i))
            self.assertTrue(i in ll)

        self.assertFalse(666 in ll)

    def testGetItem(self):
        l = [1, 202, 33, 64, 5]
        ll = LinkedList()
        for i in l:
            ll.add_to_head(i)

        for index, item in enumerate(reversed(l)):
            self.assertEqual(item, ll[index])

    def testGetItemFailure(self):
        l = [1, 202, 33, 64, 5]
        ll = LinkedList()
        for i in l:
            ll.add_to_head(i)

        with self.assertRaises(TypeError):
            ll["abc"]

        with self.assertRaises(ValueError):
            ll[-1]

        with self.assertRaises(ValueError):
            ll[ll.size]

    @unittest.skip("setitem() not implemented")
    def testSetItem(self):
        ll = LinkedList()
        ll[0] = 10

    def testRemove(self):
        l = [1, 202, 33, 64, 5]
        ll = LinkedList()
        for i in l:
            ll.add_to_head(i)

        for i in l:
            print(f"removing {i}")
            lcopy = copy.deepcopy(l)
            llcopy = copy.deepcopy(ll)
            lcopy.remove(i)
            lcopy.reverse()
            llcopy.remove(i)
            self.assertEqual(lcopy, [d for d in llcopy])
            self.assertEqual(len(lcopy), len(llcopy))

    def testRemoveFailure(self):
        ll = LinkedList()
        with self.assertRaises(KeyError):
            ll.remove(123)


class OrderedLinkedListTestCase(unittest.TestCase):
    # Added 4/5/21: made it easier to initialize the list
    def testInitWithIterable(self):
        data = [4, 2, 9]
        sorted_data = sorted(data)
        ll = OrderedLinkedList(data)
        self.assertEqual(len(data), len(ll))
        for i in range(len(sorted_data)):
            self.assertEqual(sorted_data[i], ll[i])

    def testAddOrdered(self):
        data = [3, 1, 202, 33, 64, 5]
        l = sorted(data)
        ll = OrderedLinkedList()
        for d in data:
            ll.add(d)

        self.assertEqual(len(l), ll.size)
        self.assertEqual(l, [d for d in ll])

    def testFind(self):
        l = [1, 202, 33, 64, 5]
        ll = OrderedLinkedList()
        for i in l:
            ll.add(i)

        for i in l:
            actual = ll.find(i)
            self.assertEqual(i, actual)

    def testFindFailure(self):
        ll = OrderedLinkedList()

        with self.assertRaises(KeyError):
            ll.find("no there")
