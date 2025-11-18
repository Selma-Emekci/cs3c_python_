"""
CS3C, Assignment #8, Analyzing Shellsort's Gaps
Selma EMekci

All automated tests, performance measurements, and written
analysis for Assignment 8.
"""
import random
import timeit
import unittest
from sort import shell_sort, shell_sort_hibbard
from sort_test import ShellSortTestCase
from assignment08 import *

class BaselineShellSortTestCase(ShellSortTestCase):
    """
    Baseline tests for Shell sort using Shell's original gap sequence.
    """
    def testPerformance(self):
        """
        Baseline performance for shell_sort() with Shell's original gaps.

        I measured shell_sort() on random integer lists of sizes 50000, 
        100000, and 150000. For each size, I generated a list of distinct 
        integers using random.sample() and then called helpTestPerformance(),
        which times sort_func on that list.

        The times on this environment were:
            n           Runtime (sec)
            50,000      0.177096 seconds
            100,000     0.386070 seconds
            150,000     0.675755 seconds

        My observations:
            1. The running time is not a a linear function. Increasing
               n from 50,000 to 100,000 (a factor of 2) increases time by a
               factor of about 2.18, and increasing n from 100,000 to 150,000
               (a factor of 1.5) increases time by about 1.75. This isslower
               than an O(n) algorithm, but much better than an O(n^2) algorithm.
            2. The data is consistent with the usual empirical description of
               Shell sort: worst-case O(n^2) but much better on random data.
               Growth looks qualitatively closer to n^(3/2) behaviour than to 
               pure quadratic, which is in line with the theoretical gaps.
            3. Any new gap sequence that consistently beats 0.177/0.386/0.676 
               seconds on the same input sizes can be considered an improvement 
               over Shell's original gaps on random data.
        """
        for length in (50_000, 100_000, 150_000):
            sample = random.sample(range(1_000_000_000), length)
            self.helpTestPerformance(sample)

    def testShellSortPerformanceNonPowerOf2(self):
        """
        Power-of-two vs non-power-of-two worst-case behaviour for Shell gaps.

        A worst-case input for Shell sort with original gaps is when the list 
        length is an exact power of two. When the gaps are all powers of two, 
        even and odd positions never mix until the final gap-1 pass. As a 
        result, the last insertion-sort-like phase has to do nearly all of the 
        work, and the running time becomes O(n^2).

        I compared two alternating lists:
            n_power = 8192  (exact power of two)
            n_nonpower = 9000  (nearby but not a power of two)

        Both lists are filled with the pattern [99, 1, 99, 1, ...], and I
        timed shell_sort() once on each list using timeit.
        n          Runtime (seconds)
        8192       0.727861    
        9000       0.011818  
        
        My observations:
            1. For the power-of-two length, the list stays in the adversarial
               throughout the larger-gap passes, so the final gap-1 pass 
               essentially behaves like the worst case of plain
               insertion sort on a badly ordered list. The time of about
               0.73 seconds for 8192 elements is comparable to or worse than
               the baseline timings for much larger random lists.
            2. For the non-power-of-two length, the same alternating pattern
               does not align perfectly with the powers-of-two gaps. Some even
               and odd positions start to interact earlier, so by the time
               we reach gap 1 the list is already significantly more sorted,
               and the last pass runs extremely quickly (about 0.012 seconds).
            3. A small perturbation of the length from 8192 to 9000 is enough 
               to destroy the adversarial parity structure.
        """
        n_power = 8192
        n_nonpower = 9000
        alt_power = [99, 1] * (n_power // 2)
        alt_non = [99, 1] * (n_nonpower // 2)
        if n_nonpower % 2:
            alt_non.append(99)
        t_power = timeit.timeit(lambda: shell_sort(alt_power[:]), number=1)
        t_non = timeit.timeit(lambda: shell_sort(alt_non[:]), number=1)
        print(
            f"Shell's gaps worst-case power-of-2 n={n_power}: {t_power:.6f}s, "
            f"non-power-of-2 n={n_nonpower}: {t_non:.6f}s"
        )


class ShellSortExplicitTestCase(BaselineShellSortTestCase):
    """
    Tests for shell_sort_explicit() using shells_gaps_explicit().
    """
    sort_func = shell_sort_explicit
    def testCorrectness(self):
        """
        shell_sort_explicit should produce exactly the same ordering as sorted().

        For lengths from 0 up to 99, I generate a list of distinct integers
        using random.sample(), sort a copy with Python's built-in sorted(),
        then call shell_sort_explicit() on the original list and compare the
        results. All cases in this range matched the built-in sorted() result.
        """
        for length in range(0, 100):
            sample = random.sample(range(1000), length)
            expected = sorted(sample)
            shell_sort_explicit(sample)
            self.assertEqual(expected, sample)

    def testExplicitGapsSequence(self):
        """
        Sanity check...

        The assignment states that for an input length of 11, the explicit
        Shell gaps should be [8, 4, 2, 1]. Testing whether
        shells_gaps_explicit(11) yields exactly that sequence.
        """
        self.assertEqual(list(shells_gaps_explicit(11)), [8, 4, 2, 1])

    def testPerformanceAndAnalysis(self):
        """
        Performance comparison of explicit gaps vs on-the-fly Shell gaps.

        The explicit gap sequence uses the same set of values as the original
        Shell gaps, but it reads them from a precomputed list instead of
        computing them from the length inside the sorting loop. In principle
        this should not change the asymptotic complexity at all...

        I measured shell_sort_explicit() on the same random list sizes as the
        baseline:
            Baseline shell_sort (from testPerformance):
                n             Runtime (seconds)
                50,000        0.177096
                100,000       0.386070
                150,000       0.675755

            shell_sort_explicit - run 1:
                n             Runtime
                50,000        0.555112
                100,000       1.396556
                150,000       3.817889

            shell_sort_explicit - run 2:
                n             Runtime (seconds)
                50,000        0.539560
                100,000       1.369423
                150,000       3.729398

        Several conclusions:
            1. shell_sort_explicit() is correct, but much slower than the
               baseline. For n = 150,000, the explicit version is roughly 5.5 
               times slower (around 3.8 seconds versus 0.68).
            2. The growth is still subquadratic: doubling n from
               50,000 to 100,000 multiplies time by about 2.5, and going from
               100,000 to 150,000 multiplies time by about 2.7. Constant factor 
               is much higher.
            3. A precomputed list for Shell's original gaps is not automatically 
               an improvement. The way the gaps are plugged into the generic
               shell_sort implementation introduces more overhead, possibly 
               bevause of Python-level iteration over the generator and repeated 
               slicing or indexing. In contrast, the original shells_gaps() 
               computes the next gap with a couple of integer operations and 
               appears much cheaper.

        Overall, the explicit gap sequence is not a practical performance improvement 
        over the original implementation in sort.py.
        """
        for length in (50_000, 100_000, 150_000):
            sample = random.sample(range(1_000_000_000), length)
            self.helpTestPerformance(sample)


class ShellSortSedgewickTestCase(BaselineShellSortTestCase):
    """
    Tests for shell_sort_sedgewick() and sedgewick_gaps().

    Reuses the baseline helpers but changes sort_func to the
    Sedgewick-based variant. Also includes additional tests that check
    the structure of the generated gap sequence and compare performance
    against both Shell's original gaps and Hibbard's gaps.
    """
    sort_func = shell_sort_sedgewick

    def testCorrectness(self):
        """
        shell_sort_sedgewick should sort identically to sorted().

        For lengths from 0 to 99, this test generates random lists, sorts a
        copy using sorted(), then applies shell_sort_sedgewick() to the
        original list and compares the result. All tested cases matched the 
        built-in sorted() result.
        """
        for length in range(0, 100):
            sample = random.sample(range(1000), length)
            expected = sorted(sample)
            shell_sort_sedgewick(sample)
            self.assertEqual(expected, sample)

    def testSedgewickGapsMonotone(self):
        """
        Structural properties of sedgewick_gaps().

        For lengths from 2 to 199 inclusive:
            1. The sequence is strictly decreasing when interpreted as a list.
            2. The final gap is exactly 1.
        These are required for Shell sort to work as intended:
        larger gaps first to move elements long distances, and a final gap of
        1 to finish with an ordinary insertion sort pass. The test confirms
        that our implementation of Sedgewick's formula and the manual
        insertion of gap 1 satisfy both properties across the tested range.
        """
        for length in range(2, 200):
            gaps = list(sedgewick_gaps(length))
            self.assertEqual(gaps, sorted(gaps, reverse=True))
            self.assertEqual(gaps[-1], 1)

    def testPerformanceAndAnalysis(self):
        """
        Performance comparison: Sedgewick gaps vs Shell and Hibbard gaps.

        I measured shell_sort_sedgewick() on the same random input sizes as
        the baseline and compared it to both the original Shell gaps and
        Hibbard's gaps:
            Baseline shell_sort (Shell gaps):
                n               Runtime (seconds)
                50,000          0.177096
                100,000         0.386070
                150,000         0.675755
            shell_sort_sedgewick, run 1:
                n               Runtime (seconds)
                50,000          0.151004
                100,000         0.305351
                150,000         0.484802
            shell_sort_sedgewick, run 2:
                n               Runtime (Seconds)
                50,000          0.129666
                100,000         0.291184
                150,000         0.481238

        On these random lists, Sedgewick's gaps are consistently faster than
        Shell's original gaps (roughly 15–30% speedup) and comparable to or
        slightly faster than Hibbard's gaps on this machine.
        I also compared the three sequences on the adversarial alternating
        pattern [99, 1, 99, 1, ...] of length 8192, timed with timeit:

            Shell gaps:     = 0.701930 seconds
            Hibbard gaps:   = 0.006841 seconds
            Sedgewick gaps: = 0.003711 seconds

        My observations:
            1. Shell's original gaps are vulnerable to the classic parity
               worst case and take about 0.70 seconds on this relatively
               small list.
            2. Hibbard's gaps eliminate the worst case by mixing
               positions with relatively prime gaps and improve the running
               time (down to about 0.0068 seconds).
            3. Sedgewick's gaps roughly halve the time again on this input, 
               finishing in about 0.0037 seconds.Sedgewick's theoretical advantages 
               are real constant-factor improvements for at least some non-trivial
               inputs.
        Sedgewick's gap sequence not only avoids the worst-case scenarios for Shell's 
        original gaps, butalso offers meaningful performance gains over Hibbard's 
        sequence in practice on this environment.
        """
        for length in (50_000, 100_000, 150_000):
            sample = random.sample(range(1_000_000_000), length)
            self.helpTestPerformance(sample)

        length = 8192
        worst_case = [99, 1] * (length // 2)
        duration_shell = timeit.timeit(lambda: shell_sort(worst_case[:]), number=1)
        duration_hibbard = timeit.timeit(
            lambda: shell_sort_hibbard(worst_case[:]), number=1
        )
        duration_sedgewick = timeit.timeit(
            lambda: shell_sort_sedgewick(worst_case[:]), number=1
        )
        print(
            f"Worst-case [99,1] pattern n={length}: "
            f"Shell gaps={duration_shell:.6f}s, "
            f"Hibbard gaps={duration_hibbard:.6f}s, "
            f"Sedgewick gaps={duration_sedgewick:.6f}s"
        )


class ShellSortMyTestCase(BaselineShellSortTestCase):
    """
    Tests for shell_sort_my() and my_gaps().

    Verifies correctness and then compares the custom gap sequence against 
    all of the others studied in this assignment. The main goal is to show that 
    my_gaps() is strictly better than Shell's original gaps on power-of-two 
    lengths and competitive with Hibbard's and Sedgewick's sequences on random data.
    (I think)
    """
    sort_func = shell_sort_my

    def testCorrectness(self):
        """
        For lengths from 0 to 99, this generates random lists, sorts a
        copy with sorted(), and then applies shell_sort_my() to the original
        list. All tested cases produced the same order as sorted().
        """
        for length in range(0, 100):
            sample = random.sample(range(1000), length)
            expected = sorted(sample)
            shell_sort_my(sample)
            self.assertEqual(expected, sample)

    def testMyGapsProperties(self):
        """
        Structural checks for my_gaps().
        For lengths from 2 to 199, this test asserts that:
            1. The gap list returned by my_gaps(length) is decreasing, 
               so each pass uses a smaller stride than the previous one.
            2. All gaps are positive and less than the list length, as
               required by the Shell sort invariant.
            3. The final gap is always 1, so the algorithm ends with an
               insertion sort pass that completely orders the list.
        my_gaps() is a well-formed Shell sort gap sequence.
        """
        for length in range(2, 200):
            gaps = list(my_gaps(length))
            self.assertEqual(gaps, sorted(gaps, reverse=True))
            self.assertTrue(all(0 < g < length for g in gaps))
            self.assertEqual(gaps[-1], 1)

    def testPerformanceAndAnalysis(self):
        """
        Performance comparison: my custom gaps vs Shell, Hibbard, and Sedgewick.
        Random data
        On random integer lists of sizes 50000, 100000, and 150000, the
        measured times for shell_sort_my() were:
            shell_sort_my, run 1:
                n          Runtime (Seconds)       
                50,000     0.115131
                100,000    0.244665
                150,000    0.419878
            shell_sort_my, run 2:
                n          Runtime (seconds)
                50,000     0.113022
                100,000    0.251794
                150,000    0.401586
        Comparing to the baseline Shell gaps:
            Baseline shell_sort:
                n          RUntime (seconds)
                50,000     0.177096
                100,000    0.386070
                150,000    0.675755

        My gaps are consistently faster by a comfortable margin,
        cutting the time by about one third to one half. They are also
        competitive with Sedgewick's times (around 0.15, 0.30, 0.48 seconds),
        and they are slightly faster for the largest size.

        Adversarial alternating pattern
        For the alternating pattern [99, 1, 99, 1, ...] of length 8192, the
        measured times were:
            Shell gaps:   = 0.692447 seconds
            My gaps:      = 0.005910 seconds

        My observations:
            1. The custom geometric gaps eliminate the classic
               even/odd worst case that slows Shell's original gaps.
               The time drops from about 0.69 seconds to about 0.006 seconds.
            2. The resulting time is in the same range as Hibbard's and
               Sedgewick's sequences on similar adversarial inputs, showing
               that my_gaps() avoids the worst case but does so at
               a very competitive constant factor.

        Overall conclusion
        The my_gaps() sequence satisfies the assignment requirement that our
        custom gaps outperform Shell's original gaps on power-of-two lengths,
        and it also performs well on random data. The combination of a
        simple geometric rule, avoidance of pure powers of two, and a final
        gap of 1 appears to be enough to achieve both robustness and speed
        without introducing complex formulas or precomputed tables.
        """
        for length in (50_000, 100_000, 150_000):
            sample = random.sample(range(1_000_000_000), length)
            self.helpTestPerformance(sample)

        length = 8192
        worst_case = [99, 1] * (length // 2)
        duration_shell = timeit.timeit(lambda: shell_sort(worst_case[:]), number=1)
        duration_my = timeit.timeit(lambda: shell_sort_my(worst_case[:]), number=1)
        print(
            f"My gaps vs Shell gaps on [99,1] pattern n={length}: "
            f"Shell gaps={duration_shell:.6f}s, "
            f"My gaps={duration_my:.6f}s"
        )

if __name__ == "__main__":
    unittest.main()