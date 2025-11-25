"""
CS3C, quick sort tests
Copyright 2024 Zibin Yang (5/23/2024)
"""
import random
import sys
import threading
from timeit import timeit
import unittest
import itertools
import matplotlib.pyplot as plt
from sort_test import SortTestCase
from quicksort import *


class QuickSortGenericTestCase(SortTestCase):
    @unittest.skip("Performance measurement takes time")
    def testWorstCasePerformance(self):
        # Need higher recursion limit for worst-case scenario for quick-sort
        sys.setrecursionlimit(10 ** 6)
        print("Worst case (for quick sort) performance")
        for length in itertools.chain([10, 100, 500], range(1000, 20000, 2000)):
            sample = list(range(length))
            self.helpTestPerformance(sample)


class QuickSortElTestCase(QuickSortGenericTestCase):
    sort_func = quick_sort_el


class QuickSort1eTestCase(QuickSortGenericTestCase):
    sort_func = quick_sort_1e


class QuickSortTestCase(QuickSortGenericTestCase):
    sort_func = quick_sort

    @unittest.skip("Performance comparisons take time")
    def testPerformanceComparison(self):
        def test():
            lengths = range(1000, 10000, 2000)

            print("Running random...")
            durations_random = [
                timeit(lambda: self.__class__.sort_func(random.sample(range(length * 10), length)), number=1)
                for length in lengths]
            plt.plot(lengths, durations_random, label="random")

            print("Running sorted...")
            durations_sorted = [timeit(lambda: self.__class__.sort_func(list(range(length))), number=1)
                                for length in lengths]
            plt.plot(lengths, durations_sorted, label="sorted")

            print("Running same...")
            durations_same = [timeit(lambda: self.__class__.sort_func([10] * length), number=1)
                              for length in lengths]
            plt.plot(lengths, durations_same, label="same")
            plt.legend()
            plt.xlabel("length")
            plt.ylabel("duration")
            plt.title("quick sort")
            plt.show()

        # Need higher recursion limit for worst-case scenario for quick-sort.
        # Also seems to need to increase stack size on Windows?
        sys.setrecursionlimit(10 ** 6)
        threading.stack_size(10 ** 8)
        test_thread = threading.Thread(target=test)
        test_thread.start()


class QuickSortIsTestCase(QuickSortGenericTestCase):
    sort_func = quick_sort_is


class QuickSortM3TestCase(QuickSortGenericTestCase):
    sort_func = quick_sort_m3


# Comment this out if QuickSortGenericTestCase is imported to other files.
del QuickSortGenericTestCase
del SortTestCase
