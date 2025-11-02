"""
CS3C, Assignment #6 tests
<your name here>

This file contains:
- MoreMinHeapTestCase:
    * assertIsMinHeap(minheap): validates the heap-order property across the array
      and checks len invariants.
    * tests using assertIsMinHeap() to catch invalid heaps.
    * testInsertRemoveRandom(): randomized robustness test (>=1000 ops).
    * [Extra credit] testFloydVsWilliam(): timing + percolation-count comparison.
- MedianHeapTestCase:
    * Unit tests for MedianHeap, including edge cases (0/1/2/3 items) and sample.
"""

import random
import time
import unittest

from minheap import MinHeap   # provided
from assignment06 import InstrumentedMinHeap, MedianHeap


class MoreMinHeapTestCase(unittest.TestCase):
    # ---------------------------
    # Problem 1: assertIsMinHeap
    # ---------------------------
    def assertIsMinHeap(self, minheap: MinHeap):
        """
        Verifies:
        - len(minheap) == len(minheap._heap) - 1
        - For every parent i (1..len//2), heap[i] <= heap[2*i] and (if exists) heap[i] <= heap[2*i+1]
        Does NOT check the "complete" property explicitly (array encoding guarantees it).
        """
        # length invariant
        self.assertEqual(len(minheap), len(minheap._heap) - 1)

        # heap-order property for all internal nodes
        n = len(minheap)
        for i in range(1, (n // 2) + 1):
            left = 2 * i
            right = left + 1
            if left <= n:
                self.assertLessEqual(minheap._heap[i], minheap._heap[left],
                                     msg=f"heap-order violated at parent {i} -> left {left}")
            if right <= n:
                self.assertLessEqual(minheap._heap[i], minheap._heap[right],
                                     msg=f"heap-order violated at parent {i} -> right {right}")

    def test_invalid_heap_detects_violation(self):
        # Start with a valid heap
        h = MinHeap([5, 9, 3, 7, 1, 12, 8])
        self.assertIsMinHeap(h)  # should be valid

        # Break heap-order at a parent-child pair
        # Put a huge number at the root's left child to keep order, then violate by shrinking root
        h._heap[1] = 10
        h._heap[2] = 1  # now heap[1] > heap[2] → violation
        with self.assertRaises(AssertionError):
            self.assertIsMinHeap(h)

    def test_len_mismatch_detects(self):
        h = MinHeap()
        h.insert(10)
        # Corrupt internal array length invariant by appending a stray element
        h._heap.append(9999)
        with self.assertRaises(AssertionError):
            self.assertIsMinHeap(h)

    def testInsertRemoveRandom(self):
        random.seed(12345)
        h = MinHeap()
        values = [random.randint(-10**6, 10**6) for _ in range(1000)]

        # insert phase: check heap after every insert
        seen = []
        for v in values:
            h.insert(v)
            seen.append(v)
            self.assertIsMinHeap(h)
            # peek should equal the running minimum
            self.assertEqual(min(seen), h.peek())

        # remove phase: ensure nondecreasing order and heap is valid after each removal
        removed = []
        while True:
            try:
                x = h.remove()
            except IndexError:
                break
            removed.append(x)
            self.assertIsMinHeap(h)
        # removed should be sorted
        self.assertEqual(removed, sorted(values))


    # ----------------------------------------------
    # [Extra credit] Floyd vs. William performance
    # ----------------------------------------------
    def testFloydVsWilliam(self):
        """
        Extra credit performance experiment comparing:
          - Floyd's method (heapify in __init__)
          - William's method (insert items one by one)

        We measure both wall-clock time and *data movement* counts inside
        percolation using InstrumentedMinHeap.

        To inspect results, run this test directly (it prints a small table).
        You can also copy the console table into your submission write-up.

        EXPECTATIONS (qualitative, not strictly asserted by time):
        - Average-case inputs: Floyd tends to be faster and incur fewer data moves.
        - "Worst-case" for William (descending inserts): gap widens as n grows.
        - Asymptotically: Floyd heapify is O(n); William total inserts is O(n log n).

        NOTE: We intentionally keep assertions on counts mild to avoid flakes on
        tiny sizes or slow machines; the printed table is the primary deliverable.
        """
        random.seed(42)

        def run_trials(sizes, make_data):
            rows = []
            for n in sizes:
                data = make_data(n)

                # Floyd: build heap in __init__
                hf = InstrumentedMinHeap()  # empty first to reset counters cleanly
                t0 = time.perf_counter()
                hf = InstrumentedMinHeap(data)  # this runs _order_heap() → percolate_down
                t1 = time.perf_counter()
                floyd_time = t1 - t0
                floyd_moves = hf.down_moves  # percolate_down only
                # William: insert one by one into empty heap
                hw = InstrumentedMinHeap()
                t2 = time.perf_counter()
                for x in data:
                    hw.insert(x)  # percolate_up
                t3 = time.perf_counter()
                william_time = t3 - t2
                william_moves = hw.up_moves

                rows.append((n, floyd_time, william_time, floyd_moves, william_moves))
            return rows

        sizes = [2_000, 4_000, 8_000]

        # Average-case: random data
        avg_rows = run_trials(sizes, lambda n: [random.randint(-10**7, 10**7) for _ in range(n)])
        # "Worst-case" for William: strictly descending inserts into an empty min-heap
        worst_rows = run_trials(sizes, lambda n: list(range(n, 0, -1)))

        # Light sanity assertions on movement counts (worst-case should favor Floyd)
        for (n, ft, wt, fm, wm) in worst_rows:
            self.assertGreater(wm, fm, f"Expected William moves > Floyd moves for worst-case n={n}")

        # Print a compact report (ok in tests; graders can ignore the stdout)
        def fmt(rows, title):
            print(f"\n{title}")
            print("   n        Floyd_time   William_time   Floyd_moves   William_moves")
            for n, ft, wt, fm, wm in rows:
                print(f"{n:6d}   {ft:12.6f}   {wt:12.6f}   {fm:12d}   {wm:14d}")

        fmt(avg_rows,   "AVG-CASE (random)")
        fmt(worst_rows, "WORST-CASE (descending)")
        # No strict time assertions due to environment variance.


class MedianHeapTestCase(unittest.TestCase):
    # Edge cases first
    def test_empty(self):
        mh = MedianHeap()
        with self.assertRaises(IndexError):
            mh.peek()
        with self.assertRaises(IndexError):
            mh.remove()

    def test_singleton(self):
        mh = MedianHeap([7])
        self.assertEqual(1, len(mh))
        self.assertEqual(7, mh.peek())
        self.assertEqual(7, mh.remove())
        self.assertEqual(0, len(mh))

    def test_two_elements(self):
        mh = MedianHeap([9, 2])   # sorted: [2,9], median index=1 -> 9
        self.assertEqual(2, len(mh))
        self.assertEqual(9, mh.peek())
        self.assertEqual(9, mh.remove())
        self.assertEqual(1, len(mh))
        self.assertEqual(2, mh.peek())

    def test3Elements1(self):
        # Provided sample
        list_of_data = [3, 2, 1]
        median_heap = MedianHeap(list_of_data)
        self.assertEqual(3, len(median_heap))
        self.assertEqual(2, median_heap.peek())
        self.assertEqual(2, median_heap.remove())
        self.assertEqual(3, median_heap.peek())
        self.assertEqual(3, median_heap.remove())
        self.assertEqual(1, median_heap.peek())
        self.assertEqual(1, median_heap.remove())
        self.assertEqual(0, len(median_heap))

    def test_growing_and_shrinking(self):
        mh = MedianHeap()
        nums = [7, 9, 6, 2, 5, 10, 1, 8, 3, 4]  # 10 items
        for x in nums:
            mh.insert(x)
            # median should match index len//2 of sorted prefix
            s = sorted(nums[:nums.index(x)+1])
            self.assertEqual(s[len(s)//2], mh.peek())

        # Remove all medians, they should follow “upper median” progression
        seq = []
        while True:
            try:
                seq.append(mh.remove())
            except IndexError:
                break

        # Verify by simulating “take median (upper), remove it” on a list
        tmp = sorted(nums)
        expected = []
        while tmp:
            m = tmp[len(tmp)//2]
            expected.append(m)
            tmp.pop(len(tmp)//2)
        self.assertEqual(expected, seq)
