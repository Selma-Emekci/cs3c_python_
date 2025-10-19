"""
CS3C, Assignment #4 Tests, Lazy Deletion in Binary Search Trees
Selma Emekci
Tests for my Lazy Deletion impplementation in Binary Search Trees
"""

import unittest

from assignment04 import LazyBinarySearchTree, LazyBinaryTreeNode
from bst import BinarySearchTree  # for exceptions & baseline behaviors


class LazyBSTBaseCase(unittest.TestCase):
    def make_tree(self, values):
        t = LazyBinarySearchTree()
        for v in values:
            t.insert(v)
        return t

    def assert_inorder(self, tree, expected, physical=False):
        got = list(tree.__iter__(physical=physical))
        self.assertEqual(got, expected)


class TestLazyBinaryTreeNode(LazyBSTBaseCase):
    def test_deleted_flag_and_str_repr(self):
        n = LazyBinaryTreeNode(10)
        self.assertFalse(n.deleted)
        self.assertIn("deleted=False", repr(n))

        n.deleted = True
        self.assertTrue(n.deleted)
        # __str__ must display the (D) tag
        self.assertTrue(str(n).endswith("(D)"))
        self.assertIn("deleted=True", repr(n))


class TestInsertAndRemove(LazyBSTBaseCase):
    def test_insert_increments_both_sizes_first_time(self):
        t = LazyBinarySearchTree()
        self.assertEqual(t.size, 0)
        self.assertEqual(t.size_physical, 0)

        self.assertTrue(t.insert(5))
        self.assertEqual(t.size, 1)
        self.assertEqual(t.size_physical, 1)

        self.assertFalse(t.insert(5))
        self.assertEqual(t.size, 1)
        self.assertEqual(t.size_physical, 1)

    def test_remove_soft_deletes_and_decrements_logical_size(self):
        t = self.make_tree([10, 5, 15])

        self.assertEqual(t.size, 3)
        self.assertEqual(t.size_physical, 3)

        t.remove(5) 
        self.assertEqual(t.size, 2)
        self.assertEqual(t.size_physical, 3)

        with self.assertRaises(BinarySearchTree.NotFoundError):
            t.remove(42)

        with self.assertRaises(BinarySearchTree.NotFoundError):
            t.remove(5)

    def test_insert_undeletes_if_previously_soft_deleted(self):
        t = self.make_tree([10, 5, 15])
        t.remove(5)

        self.assertTrue(t.insert(5))
        self.assertEqual(t.size, 3)
        self.assertEqual(t.size_physical, 3)

        self.assertFalse(t.insert(5))
        self.assertEqual(t.size, 3)
        self.assertEqual(t.size_physical, 3)

    def test_nodes_are_lazy_node_type(self):
        t = self.make_tree([2, 1, 3])
        self.assertIsInstance(t._root, LazyBinaryTreeNode)
        self.assertIsInstance(t._root.left_child, LazyBinaryTreeNode)
        self.assertIsInstance(t._root.right_child, LazyBinaryTreeNode)


class TestFindAndMinMax(LazyBSTBaseCase):
    def test_find_skips_deleted(self):
        t = self.make_tree([20, 10, 30, 5, 15, 25, 35])
        self.assertEqual(t.find(25), 25)
        t.remove(25)
        with self.assertRaises(BinarySearchTree.NotFoundError):
            t.find(25)

    def test_find_min_and_max_with_deletions(self):
        vals = [20, 10, 30, 5, 15, 25, 35]
        t = self.make_tree(vals)
        self.assertEqual(t.find_min(), 5)
        self.assertEqual(t.find_max(), 35)

        t.remove(5)
        self.assertEqual(t.find_min(), 10)
        t.remove(35)
        self.assertEqual(t.find_max(), 30)

        for v in [10, 15, 20, 25, 30]:
            t.remove(v)
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            t.find_min()
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            t.find_max()

    def test_find_min_with_internal_deleted_candidates(self):
        t = self.make_tree([50, 30, 70, 20, 40, 10, 25])
        t.remove(10)
        t.remove(20)
        self.assertEqual(t.find_min(), 25)


class TestIteration(LazyBSTBaseCase):

    def test_inorder_yields_only_active_by_default(self):
        vals = [23, 8, 42, 4, 16, 31, 79, 56, 91]
        t = self.make_tree(vals)
        t.remove(4)
        t.remove(56)
        expected_active = sorted(set(vals) - {4, 56})
        self.assert_inorder(t, expected_active, physical=False)

    def test_inorder_physical_includes_deleted(self):
        vals = [10, 5, 15, 3, 7, 13, 17]
        t = self.make_tree(vals)
        t.remove(7)
        t.remove(13)
        self.assert_inorder(t, sorted(vals), physical=True)
        self.assert_inorder(t, sorted(set(vals) - {7, 13}), physical=False)


class TestStringAndRepr(LazyBSTBaseCase):
    def test_str_marks_deleted_nodes(self):
        vals = [10, 5, 15, 3, 7]
        t = self.make_tree(vals)
        t.remove(7)
        s = str(t)
        self.assertIn("7(D)", s)

    def test_repr_contains_sizes_and_orders(self):
        vals = [20, 10, 30, 5, 15, 25, 35]
        t = self.make_tree(vals)
        t.remove(25)
        r = repr(t)
        self.assertIn("size=", r)
        self.assertIn("size_physical=", r)
        self.assertIn("active_inorder", r)
        self.assertNotIn("25,)", r.replace(" ", ""))
        self.assertIn("physical_inorder", r)
        self.assertIn("25", r)


class TestGarbageCollection(LazyBSTBaseCase):
    def test_collect_garbage_removes_only_deleted_and_keeps_logical_size(self):
        vals = [50, 30, 70, 20, 40, 60, 80, 10, 25, 35, 45]
        t = self.make_tree(vals)
        to_delete = {10, 40, 70}
        for v in to_delete:
            t.remove(v)

        size_before = t.size
        phys_before = t.size_physical

        self.assertEqual(size_before, len(vals) - len(to_delete))
        self.assertEqual(phys_before, len(vals))

        t.collect_garbage()
        self.assertEqual(t.size, size_before)
        self.assertEqual(t.size_physical, phys_before - len(to_delete))
        self.assert_inorder(t, sorted(set(vals) - to_delete), physical=False)
        self.assert_inorder(t, sorted(set(vals) - to_delete), physical=True)

        for v in (set(vals) - to_delete):
            self.assertEqual(t.find(v), v)
        for v in to_delete:
            with self.assertRaises(BinarySearchTree.NotFoundError):
                t.find(v)

    def test_collect_garbage_all_deleted_results_in_empty_tree(self):
        vals = [3, 1, 4, 2]
        t = self.make_tree(vals)
        for v in vals:
            t.remove(v)

        self.assertEqual(t.size, 0)
        self.assertEqual(t.size_physical, len(vals))

        t.collect_garbage()

        self.assertEqual(t.size, 0)
        self.assertEqual(t.size_physical, 0)
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            t.find_min()
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            t.find_max()

    def test_collect_garbage_is_postorder_safe(self):
        t = self.make_tree([5, 2, 8, 1, 3])
        t.remove(2)
        t.remove(1)
        t.collect_garbage()
        self.assert_inorder(t, [3, 5, 8], physical=False)
        self.assertEqual(t.size, 3)
        self.assertEqual(t.size_physical, 3)


class TestEdgeCases(LazyBSTBaseCase):
    def test_empty_tree_min_max_and_remove(self):
        t = LazyBinarySearchTree()
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            t.find_min()
        with self.assertRaises(BinarySearchTree.EmptyTreeError):
            t.find_max()
        with self.assertRaises(BinarySearchTree.NotFoundError):
            t.remove(1)

    def test_contains_uses_find_behavior(self):
        t = self.make_tree([10, 5])
        self.assertIn(10, t)
        t.remove(10)
        self.assertNotIn(10, t)

if __name__ == "__main__":
    unittest.main()