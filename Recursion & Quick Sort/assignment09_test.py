"""
CS3C, Assignment #9, Quick sort recursion limit and pivot selection
Selma Emekci
"""
import random
import time
import unittest
import sys
from assignment09 import quick_sort_x, quick_sort_my_pivot, quick_sort_builtin
from quicksort import quick_sort_is, quick_sort_m3
sys.setrecursionlimit(10**7)

class QuickSortXCorrectnessTestCase(unittest.TestCase):
    def help_check_sort(self, sort_func):
        cases = [
            [],
            [1],
            [2, 1],
            [1, 2],
            [3, 1, 2, 5, 4],
            [5, 4, 3, 2, 1],
            [7, 7, 7, 7],
            [3, 1, 2, 3, 2, 1],
        ]
        for length in range(0, 20):
            sample = random.sample(range(1000), length)
            cases.append(sample)
        for data in cases:
            with self.subTest(data=data):
                expected = sorted(data)
                actual = list(data)
                sort_func(actual)
                self.assertEqual(expected, actual)

    def test_quick_sort_x_correctness_default_limit(self):
        self.help_check_sort(lambda a: quick_sort_x(a))

    def test_quick_sort_x_correctness_custom_limit(self):
        self.help_check_sort(lambda a: quick_sort_x(a, rec_limit=8))

    def test_quick_sort_x_invalid_limit(self):
        with self.assertRaises(ValueError):
            quick_sort_x([3, 2, 1], rec_limit=1)


class QuickSortXRecursionLimitAnalysisTestCase(unittest.TestCase):
    def testQuickSortRecursionLimit(self):
        """
        Setup
        Function: quick_sort_x() from assignment09.py.
        Timer: time.perf_counter().
        For each (n, rec_limit) pair, average of three runs on a fresh copy 
        of the base list.
        Input sizes (n): 40,000; 80,000; 160,000; 320,000.
        Collected data (seconds)
        n = 40,000
            rec_limit    time
                 2      0.0627
                 4      0.0590
                 6      0.0666
                 8      0.0566
                10      0.0564
                12      0.0566
                14      0.0569
                16      0.0575
                18      0.0579
                20      0.0584
                22      0.0591
                24      0.0597
                26      0.0604
                28      0.0612
                30      0.0620
                32      0.0624

        n = 80,000
            rec_limit    time
                 2      0.1288
                 4      0.1310
                 6      0.1232
                 8      0.1220
                10      0.1212
                12      0.1234
                14      0.1215
                16      0.1226
                18      0.1245
                20      0.1363
                22      0.1266
                24      0.1275
                26      0.1280
                28      0.1472
                30      0.1336
                32      0.1371

        n = 160,000
            rec_limit    time
                 2      0.2850
                 4      0.2936
                 6      0.2931
                 8      0.3016
                10      0.2935
                12      0.2702
                14      0.2729
                16      0.2937
                18      0.2762
                20      0.2778
                22      0.2929
                24      0.2919
                26      0.2952
                28      0.3296
                30      0.3003
                32      0.3021

        n = 320,000
            rec_limit    time
                 2      0.6641
                 4      0.6562
                 6      0.6398
                 8      0.6803
                10      0.6129
                12      0.6469
                14      0.6391
                16      0.6246
                18      0.6539
                20      0.6557
                22      0.6656
                24      0.6432
                26      0.6428
                28      0.6471
                30      0.6913
                32      0.6721

        My Observations:
        1. For all n, the timing curve over rec_limit is shallow.  There is no
           single sharp optimum, maybe a broad flat region at best.
        2. Very small rec_limit (2-4) tends to be slightly slower, especially
           for larger n, because insertion sort is applied to larger subarrays.
        3. Very large rec_limit (around 28-32) is also a bit slower on most n,
           because Quick sort keeps recursing into small nearly sorted
           partitions instead of switching to insertion sort earlier.
        4. The best or near-best times occur consistently in the middle range
           rec_limit = 8-20, with rec_limit around 12-16 performing well for
           all four n.

        Conclusion
        The data supports using a recursion limit in a middle range rather than
        an extreme.  Values between about 8 and 20 are consistently close to
        optimal across the tested sizes, and 15 (the lecture default) lies in
        this stable region.
        """
        sizes = [40000, 80000, 160000, 320000]
        limits = list(range(2, 34, 2))
        results = {}
        for n in sizes:
            base = random.sample(range(n * 10), n)
            results[n] = {}
            for rec_limit in limits:
                data = list(base)
                start = time.perf_counter()
                quick_sort_x(data, rec_limit=rec_limit)
                elapsed = time.perf_counter() - start
                results[n][rec_limit] = elapsed
        for n in sizes:
            print(f"n={n}")
            for rec_limit in limits:
                print(f"  rec_limit={rec_limit:2d}, time={results[n][rec_limit]:.4f}s")


class QuickSortPivotCorrectnessTestCase(unittest.TestCase):
    def help_check_sort(self, sort_func):
        cases = [
            [],
            [0],
            [1, 1, 1],
            [2, 1],
            [1, 2],
            [3, 1, 2, 5, 4],
            [5, 4, 3, 2, 1],
        ]
        for length in range(0, 20):
            sample = random.sample(range(1000), length)
            cases.append(sample)
        for data in cases:
            with self.subTest(data=data):
                expected = sorted(data)
                actual = list(data)
                sort_func(actual)
                self.assertEqual(expected, actual)

    def test_quick_sort_my_pivot_correctness(self):
        self.help_check_sort(lambda a: quick_sort_my_pivot(a))

    def test_quick_sort_builtin_correctness(self):
        self.help_check_sort(lambda a: quick_sort_builtin(a))


class QuickSortPivotPerformanceTestCase(unittest.TestCase):
    def testPivotPerformance(self):
        """
        Setup
        Implementations:
            quick_sort_is       – first-element pivot + insertion-sort cutoff
            quick_sort_m3       – median-of-three pivot + insertion-sort cutoff
            quick_sort_my_pivot – middle-element pivot + insertion-sort cutoff
            quick_sort_builtin  – wrapper around built-in sorted() (Timsort)
        Data sets:
            1. Random integers
            2. Already-sorted integers
        Input sizes:
            n = 50,000; 100,000; 200,000; 400,000
        Timer: time.perf_counter().
        For each (algorithm, data type, n), average of 3 runs, each on a fresh 
        copy of the base list.
        
        Measured runtimes (seconds)
        Random data
            n = 50,000
                quick_sort_is        0.0738
                quick_sort_m3        0.0987
                quick_sort_my_pivot  0.0741
                quick_sort_builtin   0.0081

            n = 100,000
                quick_sort_is        0.1753
                quick_sort_m3        0.2104
                quick_sort_my_pivot  0.1728
                quick_sort_builtin   0.0208

            n = 200,000
                quick_sort_is        0.3750
                quick_sort_m3        0.4124
                quick_sort_my_pivot  0.3775
                quick_sort_builtin   0.0383

            n = 400,000
                quick_sort_is        0.9668
                quick_sort_m3        1.1502
                quick_sort_my_pivot  0.9729
                quick_sort_builtin   0.1305

        Sorted data
            n = 50,000
                quick_sort_is       53.9289
                quick_sort_m3        0.0310
                quick_sort_my_pivot  0.0383
                quick_sort_builtin   0.0005

            n = 100,000
                quick_sort_is      210.3077
                quick_sort_m3        0.0547
                quick_sort_my_pivot  0.0712
                quick_sort_builtin   0.0012

            n = 200,000
                quick_sort_is      951.5949
                quick_sort_m3        0.1171
                quick_sort_my_pivot  0.1470
                quick_sort_builtin   0.0020

            n = 400,000
                quick_sort_is      3997.0221
                quick_sort_m3         0.2721
                quick_sort_my_pivot   0.3146
                quick_sort_builtin    0.0042

        My Obserations - Random Data
        For random data the observed ranking (fastest to slowest) is:
            1) quick_sort_builtin
            2) quick_sort_is and quick_sort_my_pivot (very close)
            3) quick_sort_m3

        All three Quick sort variants show approx O(n log n) growth.  Median-of-three
        has slightly higher constant overhead in this implementation, so on
        random input its better pivot quality does not offset the extra work
        and it is slower.  The middle-element pivot behaves almost
        the same as the first-element pivot on random data, which explains why
        quick_sort_is and quick_sort_my_pivot are close.  The builtin sort is
        much faster because it is implemented in C and uses Timsort, which is
        highly optimized and does fewer Python-level operations.

        The ranking matches expectations because all pivot schemes are
        good for random data, with differences dominated by constant factors,
        and the builtin Timsort is expected to win due to its implementation.

        My Observations - Sorted Data
        For sorted data the observed ranking (fastest to slowest) is:
            1) quick_sort_builtin
            2) quick_sort_m3
            3) quick_sort_my_pivot
            4) quick_sort_is

        quick_sort_is always picks the first element as the pivot, so on
        already-sorted input it repeatedly produces extremely unbalanced
        partitions and shows O(n^2) behaviour with very large runtimes.  Both
        quick_sort_m3 and quick_sort_my_pivot pick pivots near the middle of
        the current subarray (median-of-three vs exact middle index), so they
        keep the partitions balanced and retain O(n log n) running time. 
        quick_sort_m3 is slightly faster than the middle-element pivot, which 
        is reasonable because its median-of-three rule reduces the chance of a 
        bad pivot even when the data is not perfectly ordered.

        quick_sort_builtin is still fastest. CPython's sorted() is an adaptive 
        stable O(n log n) algorithm that detects and exploits existing ordered runs.  
        On fully sorted input Timsort does very little work, which explains the tiny 
        runtimes and the clear gap between it and the pure Python Quick sort 
        implementations.

        Summary
        Random data:
            builtin < quick_sort_is approx. = quick_sort_my_pivot < quick_sort_m3
        Sorted data:
            builtin < quick_sort_m3 < quick_sort_my_pivot << quick_sort_is

        The measurements match the theoretical: pivot choice mainly
        matters for adversarial inputs such as already-sorted lists.  The
        first-element pivot degrades to the worst case, while median-of-three
        and middle-element pivots avoid that and keep Quick sort close to its
        average-case O(n log n) performance.  The builtin Timsort is faster in
        all cases because of its optimized C implementation and adaptivity.
        """
        sizes = [50000, 100000, 200000, 400000]
        algorithms = {
            "quick_sort_is": quick_sort_is,
            "quick_sort_m3": quick_sort_m3,
            "quick_sort_my_pivot": quick_sort_my_pivot,
            "quick_sort_builtin": quick_sort_builtin,
        }

        print("Random data:")
        for n in sizes:
            base = random.sample(range(n * 10), n)
            print(f"n={n}")
            for name, func in algorithms.items():
                data = list(base)
                start = time.perf_counter()
                func(data)
                elapsed = time.perf_counter() - start
                print(f"  {name:20s}: {elapsed:.4f}s")

        print("\nSorted data:")
        for n in sizes:
            base = list(range(n))
            print(f"n={n}")
            for name, func in algorithms.items():
                data = list(base)
                start = time.perf_counter()
                func(data)
                elapsed = time.perf_counter() - start
                print(f"  {name:20s}: {elapsed:.4f}s")


if __name__ == "__main__":
    unittest.main()
