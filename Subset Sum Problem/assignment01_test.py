"""
CS3C, Assignment #1, Subset Sum (tests)
Student: Selma Emekci

Automated tests for assignment01.py using unittest.
"""

import unittest
from assignment01 import subset_sum, subset_sum_rec, subset_sum_flex
from itunes import iTunesEntryReader


class TestSubsetSum(unittest.TestCase):

    def test_empty(self):
        self.assertEqual(subset_sum([], 10), set())
        self.assertEqual(subset_sum_rec([], 10), set())

    def test_single_int(self):
        self.assertEqual(subset_sum([5], 10), {5})   # target larger
        self.assertEqual(subset_sum([5], 5), {5})    # target equal
        self.assertEqual(subset_sum([5], 3), set())  # target smaller

    def test_two_ints(self):
        nums = [3, 7]
        self.assertEqual(subset_sum(nums, 2), set())       # smaller than both
        self.assertEqual(subset_sum(nums, 5), {3})         # between them
        self.assertEqual(subset_sum(nums, 15), {3, 7})     # larger than sum

    def test_large_list(self):
        nums = [20, 12, 22, 15, 25, 19, 29, 18, 11, 13, 17]
        result = subset_sum(nums, 200)
        expected = {12, 20, 22, 15, 25, 19, 29, 18, 13, 17}  # per assignment spec
        self.assertEqual(result, expected)

    def test_specific_list(self):
        nums = [25, 27, 3, 12, 6, 15, 9, 30, 21, 19]
        result = subset_sum(nums, 50)
        self.assertEqual(result, {25, 6, 19})

    def test_duplicates_raise(self):
        with self.assertRaises(ValueError):
            subset_sum([1, 2, 2, 3], 5)

    def test_recursive_matches_iterative(self):
        nums = [5, 10, 12, 13, 15, 18]
        target = 30
        iter_subset = subset_sum(nums, target)
        rec_subset = subset_sum_rec(nums, target)
        self.assertEqual(sum(iter_subset), sum(rec_subset))


    def test_itunes(self):
        itunes = iTunesEntryReader("Subset Sum Problem/itunes_file.txt")
        result = subset_sum(itunes, 3600)
        total = sum(entry.run_time for entry in result)
        self.assertEqual(total, 3600)

    def test_flexible_lambda(self):
        # Flexible version using value_of
        nums = [10, 15, 25, 30]
        result = subset_sum_flex(nums, 40, value_of=lambda x: x)
        total = sum(result)
        self.assertLessEqual(total, 40)
        self.assertEqual(total, 40)


if __name__ == "__main__":
    unittest.main()
