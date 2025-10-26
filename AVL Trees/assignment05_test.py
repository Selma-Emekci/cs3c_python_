"""
CS3C, Assignment #5 Tests, AVL Tree
Selma Emekci
Testing on Assignment 5
"""
import random
import unittest
from assignment05 import AvlTree, AvlTreeNode

class AvlTreeTestCase(unittest.TestCase):
    TreeType = AvlTree
    def assertIsAvlTree(self, avltree):
        self.assertIsInstance(avltree, self.TreeType)
        def check(node, low, high):
            if node is None:
                return -1
            self.assertIsInstance(node, AvlTreeNode)
            if low is not None:
                self.assertLess(low, node.data, msg=f"data {node.data} not > lower bound {low}")
            if high is not None:
                self.assertLess(node.data, high, msg=f"data {node.data} not < upper bound {high}")
            lh = check(node.left_child, low, node.data)
            rh = check(node.right_child, node.data, high)
            expected_h = 1 + max(lh, rh)
            self.assertEqual(expected_h,node.height,msg=f"height mismatch at {node.data}")
            self.assertLessEqual(abs(lh - rh), 1, msg=f"AVL violation at {node.data} (lh={lh}, rh={rh})")
            return expected_h

        root =avltree._root
        check(root, None, None)

    def test_assertIsAvlTree_detects_bad_heights(self):
        t = self.TreeType()
        t._root = AvlTreeNode(2, left_child=AvlTreeNode(1), right_child=AvlTreeNode(3))
        t._root.height = 0
        t._root.left_child.height = 0
        t._root.right_child.height = 0
        with self.assertRaises(AssertionError):
            self.assertIsAvlTree(t)

    def test_assertIsAvlTree_detects_bst_violation(self):
        t = self.TreeType()
        t._root = AvlTreeNode(2, left_child=AvlTreeNode(1), right_child=AvlTreeNode(0))
        t._root.left_child.height = 0
        t._root.right_child.height = 0
        t._root.height = 1
        with self.assertRaises(AssertionError):
            self.assertIsAvlTree(t)

    def test_single_right_rotation_LL(self):
        tree = self.TreeType()
        for d in [3, 2, 1]:
            tree.insert(d)
        self.assertEqual(2, tree._root.data)
        self.assertEqual(1, tree._root.left_child.data)
        self.assertEqual(3, tree._root.right_child.data)
        self.assertIsAvlTree(tree)

    def test_single_left_rotation_RR(self):
        tree = self.TreeType()
        for d in [1, 2, 3]:
            tree.insert(d)
        self.assertEqual(2, tree._root.data)
        self.assertEqual(1, tree._root.left_child.data)
        self.assertEqual(3, tree._root.right_child.data)
        self.assertIsAvlTree(tree)

    def test_double_rotation_LR(self):
        tree = self.TreeType()
        for d in [3, 1, 2]:
            tree.insert(d)
        self.assertEqual(2, tree._root.data)
        self.assertEqual(1, tree._root.left_child.data)
        self.assertEqual(3, tree._root.right_child.data)
        self.assertIsAvlTree(tree)

    def test_double_rotation_RL(self):
        tree = self.TreeType()
        for d in [1, 3, 2]:
            tree.insert(d)
        self.assertEqual(2, tree._root.data)
        self.assertEqual(1, tree._root.left_child.data)
        self.assertEqual(3, tree._root.right_child.data)
        self.assertIsAvlTree(tree)

    def test_remove_rebalances(self):
        tree = self.TreeType()
        nums = [50, 20, 70, 10, 30, 60, 80, 25, 27]
        for n in nums:
            tree.insert(n)
        self.assertIsAvlTree(tree)
        tree.remove(10)
        self.assertIsAvlTree(tree)
        tree.remove(30)
        self.assertIsAvlTree(tree)

    def test_AvlTreeInsertRemoveRandom(self):
        tree = self.TreeType()
        random.seed(42)
        data = random.sample(range(2000), 200)
        for x in data:
            tree.insert(x)
            self.assertIsAvlTree(tree)
        final_height = tree.height
        self.assertLess(final_height, 40, msg=f"height too large for AVL: {final_height}")
        order = random.sample(data, len(data))
        for x in order:
            tree.remove(x)
            self.assertIsAvlTree(tree)

if __name__ == "__main__":
    unittest.main()
