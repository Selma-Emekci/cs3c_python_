"""
CS3C: BinarySearchTree tests
Copyright 2022 Zibin Yang
(Soft-linked in assignment)
(Do not modify or submit this file for assignments)
"""
import copy
import random
import unittest
from bst import *


class BstTestCase(unittest.TestCase):
    # Slight deviation from lecture: create a class attribute for the type
    # of tree used in the test, so the subclass (e.g. AvlTreeTestCase)
    # may override it.
    TreeType = BinarySearchTree

    def testInit(self):
        bst = self.TreeType()
        self.assertIsNone(bst._root)
        self.assertEqual(0, bst.size)
        self.assertEqual(0, len(bst))

    def testInitWithData(self):
        initial_data = [4, 7, 2, 1, 3]
        bst = self.TreeType(initial_data)
        self.assertListEqual(sorted(initial_data), [item for item in bst])

    def testInsert(self):
        bst = self.TreeType()

        bst.insert(23)
        self.assertEqual(23, bst._root.data)
        self.assertIsNone(bst._root.left_child)
        self.assertIsNone(bst._root.right_child)
        self.assertEqual(1, bst.size)

        bst.insert(8)
        self.assertEqual(23, bst._root.data)
        self.assertEqual(8, bst._root.left_child.data)
        self.assertIsNone(bst._root.right_child)
        self.assertEqual(2, bst.size)

        bst.insert(42)
        self.assertEqual(23, bst._root.data)
        self.assertEqual(8, bst._root.left_child.data)
        self.assertEqual(42, bst._root.right_child.data)
        self.assertEqual(3, bst.size)

        bst.insert(4)
        self.assertEqual(23, bst._root.data)
        self.assertEqual(8, bst._root.left_child.data)
        self.assertEqual(42, bst._root.right_child.data)
        self.assertEqual(4, bst._root.left_child.left_child.data)
        self.assertEqual(4, bst.size)

    def testInsertDuplicate(self):
        bst = self.TreeType()
        bst.insert(11)
        with self.assertRaises(BinarySearchTree.DuplicateDataError):
            bst.insert(11)

    def testStr(self):
        bst = self.TreeType()
        bst.insert(23)
        bst.insert(8)
        bst.insert(42)
        bst.insert(4)
        print(bst)

    def testRepr(self):
        print(repr(self.tree))

    def testIter(self):
        bst = self.TreeType()
        self.assertEqual([], [d for d in bst], "empty tree")

        data = [23, 8, 42, 4]
        for d in data:
            bst.insert(d)

        actual = [d for d in bst]
        self.assertEqual(sorted(data), actual)

    def testSum(self):
        bst = self.TreeType()
        self.assertEqual(0, sum(bst), "empty tree")

        data = [23, 8, 42, 4]
        for d in data:
            bst.insert(d)

        self.assertEqual(sum(data), sum(bst))

    def setUp(self):
        # Slight deviation from lecture: call this a generic tree rather
        # than tying it to a bst.
        self.tree = self.TreeType()
        self.data = [23, 8, 42, 4, 1]
        for d in self.data:
            self.tree.insert(d)

    def testFind(self):
        for d in self.data:
            actual = self.tree.find(d)
            self.assertEqual(d, actual)

    def testFindFailure(self):
        bst = self.TreeType()
        with self.assertRaises(BinarySearchTree.NotFoundError):
            bst.find("nothing in empty tree")

        data = [23, 8, 42, 4]
        for d in data:
            bst.insert(d)

        with self.assertRaises(BinarySearchTree.NotFoundError):
            bst.find(777)

    def testFindMinEmptyBst(self):
        bst = self.TreeType()
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            bst.find_min()

    def testFindMin(self):
        bst = self.TreeType()
        data = [23, 8, 42, 4]
        expected = []
        for d in data:
            expected.append(d)
            bst.insert(d)
            self.assertEqual(min(expected), bst.find_min())

    def testFindMaxEmptyBst(self):
        bst = self.TreeType()
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            bst.find_max()

    def testFindMax(self):
        bst = self.TreeType()
        data = [23, 8, 42, 4]
        expected = []
        for d in data:
            expected.append(d)
            bst.insert(d)
            self.assertEqual(max(expected), bst.find_max())

    def testRemove1(self):
        bst = self.TreeType()
        data = [23, 8, 42, 4, 31, 79, 56, 91]
        for d in data:
            bst.insert(d)
        print(bst)

        data.remove(23)
        bst.remove(23)
        print(bst)
        actual = [d for d in bst]
        self.assertEqual(sorted(data), actual)
        self.assertEqual(len(data), len(bst))

    def testRemove(self):
        bst = self.TreeType()
        random.seed(123)
        data = random.sample(range(1000), 100)
        for d in data:
            # print(repr(bst))
            # print(f"inserting {d}")
            bst.insert(d)

        data_to_remove = random.sample(data, len(data))
        # print(f"data={data}")
        # print(f"data_to_remove={data_to_remove}")

        for d in data_to_remove:
            with self.subTest(f"remove({d})"):
                data.remove(d)
                bst.remove(d)
                # print(bst)
                actual = [d for d in bst]
                self.assertEqual(sorted(data), actual)
                self.assertEqual(len(data), len(bst))

                with self.assertRaises(BinarySearchTree.NotFoundError):
                    bst.remove(d)

    def testUnbalancedBst(self):
        bst = self.TreeType()
        for i in range(10):
            bst.insert(i)
        print(bst)

    # Optional: test for traverse()
    def testTraverse(self):
        # Demo how to use traverse() to sum up everything in bst, but using
        # __iter__() is much simpler (see testSum())
        expected = sum(self.data)
        actual = self.tree.traverse(lambda result, data: result + data, 0)
        print(f"bst is:\n{self.tree}")
        print(f"sum is {actual}")
        self.assertEqual(expected, actual)
