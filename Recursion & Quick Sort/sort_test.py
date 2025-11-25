"""
CS3C, sorting algorithms tests
Copyright 2021 Zibin Yang
"""
import itertools
import random
import timeit
import unittest

from sort import *


class SortTestCase(unittest.TestCase):
    sort_func = None

    def setUp(self):
        # Reproducible random number generation
        random.seed(3)

    def helpTestSort(self, iterable):
        sorted_iterable = sorted(iterable)
        # Cannot do self.sort_function(), which would implicitly pass self as
        # the first parameter to sort_function()
        self.__class__.sort_func(iterable)
        self.assertEqual(sorted_iterable, iterable)

    def testSortEmpty(self):
        self.helpTestSort([])

    def testSortLen1(self):
        self.helpTestSort([99])

    def testSortLen2(self):
        self.helpTestSort([88, 99])
        self.helpTestSort([99, 88])

    def testSortLen5(self):
        self.helpTestSort([99, 55, 88, 66, 11])

    def testSortSorted(self):
        self.helpTestSort(list(range(100)))

    def testSortSame(self):
        self.helpTestSort([10] * 100)

    def testSortAllLengths(self):
        for length in range(100):
            sample = random.sample(range(1000), length)
            with self.subTest(f"Testing sort length={length}, sample={sample}"):
                self.helpTestSort(sample)

    @unittest.skip("Skipping performance test")
    def testPerformance(self):
        for length in itertools.chain([10, 100, 500], range(1000, 20000, 2000)):
            sample = random.sample(range(1000000), length)
            self.helpTestPerformance(sample)

    def helpTestPerformance(self, sample):
        duration = timeit.timeit(lambda: self.__class__.sort_func(sample), number=1)
        print(f"{self.__class__.sort_func.__name__} on {len(sample)} "
              f"items takes {duration:.6f} seconds")


class BubbleSortTestCase(SortTestCase):
    sort_func = bubble_sort


class InsertionSortTestCase(SortTestCase):
    sort_func = insertion_sort


class ShellSortTestCase(SortTestCase):
    sort_func = shell_sort

    @unittest.skip("Performance tests take time")
    def testShellSortPerformanceOddEven(self):
        length = 128
        while length < 20000:
            sample = [1, 99] * (length // 2)
            self.helpTestPerformance(sample)
            length *= 2

    @unittest.skip("Performance tests take time")
    def testShellSortPerformanceRandom(self):
        length = 128
        while length < 20000:
            sample = random.sample(range(1000000), length)
            self.helpTestPerformance(sample)
            length *= 2


class ShellSortHibbardTestCase(ShellSortTestCase):
    sort_func = shell_sort_hibbard


class MergeSortTestCase(SortTestCase):
    sort_func = merge_sort


class GapsTestCase(unittest.TestCase):
    def testHibbards1(self):
        length = 128
        print(f"Hibbard's gaps up to {length}")
        for gap in hibbards_gaps(length):
            print(gap)

    def testHibbards2(self):
        length = 100
        print(f"Hibbard's gaps up to {length}")
        for gap in hibbards_gaps(length):
            print(gap)


# This has to be commented out if it's imported to other tests.
del SortTestCase
