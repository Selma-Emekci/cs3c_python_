"""
CS3C, Assignment #2, Sparse Matrices (Tests)
Selma Emekci
Screaming crying throwing up aggggggghhhhhhhh
"""

import unittest
from assignment02 import SparseMatrix


class SparseMatrixBasicsTests(unittest.TestCase):
    """
    Testing my SparseMatrix according to assignment specificication.
    """
    def test_defaults_and_str_and_rowlist_len(self):
        sm = SparseMatrix(2, 3, -1)
        self.assertEqual(str(sm), "-1 -1 -1\n-1 -1 -1")
        self.assertEqual(len(sm._get_row_list(0)), 0)

        sm.set(0, 1, 100)
        self.assertEqual(str(sm), "-1 100 -1\n-1 -1 -1")
        self.assertEqual(len(sm._get_row_list(0)), 1)

    def test_get_set_update_remove(self):
        sm = SparseMatrix(3, 4, 0)
        self.assertEqual(sm.get(2, 3), 0)  # default from unset

        sm.set(2, 3, 7)
        self.assertEqual(sm.get(2, 3), 7)

        sm.set(2, 3, 9)  # update
        self.assertEqual(sm.get(2, 3), 9)

        sm.set(2, 3, 0)
        self.assertEqual(sm.get(2, 3), 0)
        self.assertEqual(len(sm._get_row_list(2)), 0)

    def test_multiple_in_row_and_generators(self):
        sm = SparseMatrix(2, 4, 0)
        sm.set(0, 0, 5)
        sm.set(0, 2, 7)
        sm.set(1, 3, 9)

        self.assertEqual(list(sm.get_row(0)), [5, 0, 7, 0])
        self.assertEqual(list(sm.get_row(1)), [0, 0, 0, 9])

        self.assertEqual(list(sm.get_col(0)), [5, 0])
        self.assertEqual(list(sm.get_col(2)), [7, 0])
        self.assertEqual(list(sm.get_col(3)), [0, 9])

    def test_invalid_indices(self):
        sm = SparseMatrix(2, 2, 0)

        with self.assertRaises(IndexError):
            sm.get(10, 0)
        with self.assertRaises(IndexError):
            sm.get(0, 10)
        with self.assertRaises(IndexError):
            sm.set(-1, 0, 1)
        with self.assertRaises(IndexError):
            sm.set(0, -1, 1)

        with self.assertRaises(IndexError):
            list(sm.get_row(10))
        with self.assertRaises(IndexError):
            list(sm.get_col(10))


if __name__ == "__main__":
    unittest.main()
