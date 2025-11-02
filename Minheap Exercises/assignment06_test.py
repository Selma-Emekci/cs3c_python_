"""
CS3C, Assignment #6 Tests, Test for MinHeap Exercises
Selma Emekci
Tests for MinHeap Exercises
"""
import random
import time
import unittest
from minheap import MinHeap
from assignment06 import InstrumentedMinHeap, MedianHeap

class MoreMinHeapTestCase(unittest.TestCase):
    def assertIsMinHeap(self, minheap: MinHeap):
        """
        index 0 sentinel is None
        len(minheap) == len(minheap._heap) - 1
        Does NOT check the "complete" property (array encoding guarantees)
        """
        self.assertIsNone(minheap._heap[0], "index 0 sentinel must be None")
        self.assertEqual(len(minheap), len(minheap._heap) - 1)
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
        h = MinHeap([5, 9, 3, 7, 1, 12, 8])
        self.assertIsMinHeap(h)
        h._heap[1] = 10
        h._heap[2] = 1
        with self.assertRaises(AssertionError):
            self.assertIsMinHeap(h)

    def test_index0_sentinel_detects_corruption(self):
        h = MinHeap([5, 9, 3, 7, 1, 12, 8])
        self.assertIsMinHeap(h)
        h._heap[0] = 123
        with self.assertRaises(AssertionError):
            self.assertIsMinHeap(h)

    def testInsertRemoveRandom(self):
        random.seed(12345)
        h = MinHeap()
        values = [random.randint(-10**6, 10**6) for _ in range(1000)]
        seen = []
        for v in values:
            h.insert(v)
            seen.append(v)
            self.assertIsMinHeap(h)
            self.assertEqual(min(seen), h.peek())
        removed = []
        while True:
            try:
                x = h.remove()
            except IndexError:
                break
            removed.append(x)
            self.assertIsMinHeap(h)
        self.assertEqual(removed, sorted(values))
    
    def testFloydVsWilliam(self):
        random.seed(42)
        def run_trials(sizes, make_data):
            rows = []
            for n in sizes:
                data = make_data(n)
                t0 = time.perf_counter()
                hf = InstrumentedMinHeap(data)
                t1 = time.perf_counter()
                floyd_time = t1 - t0
                floyd_moves = hf.down_moves

                hw = InstrumentedMinHeap()
                t2 = time.perf_counter()
                for x in data:
                    hw.insert(x)
                t3 = time.perf_counter()
                william_time = t3 - t2
                william_moves = hw.up_moves
                rows.append((n, floyd_time, william_time, floyd_moves, william_moves))
            return rows
        
        sizes = [2_000, 4_000, 8_000]
        avg_rows = run_trials(sizes, lambda n: [random.randint(-10**7, 10**7) for _ in range(n)])
        worst_rows = run_trials(sizes, lambda n: list(range(n, 0, -1)))
        for (n, ft, wt, fm, wm) in worst_rows:
            self.assertGreater(wm, fm, f"Expected William moves > Floyd moves for worst-case n={n}")
        
        def fmt(rows, title):
            print(f"\n{title}")
            print("   n        Floyd_time   William_time   Floyd_moves   William_moves")
            for n, ft, wt, fm, wm in rows:
                print(f"{n:6d}   {ft:12.6f}   {wt:12.6f}   {fm:12d}   {wm:14d}")
        fmt(avg_rows,   "AVG-CASE (random)")
        fmt(worst_rows, "WORST-CASE (descending)")

class MedianHeapTestCase(unittest.TestCase):
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
        mh = MedianHeap([9, 2])
        self.assertEqual(2, len(mh))
        self.assertEqual(9, mh.peek())
        self.assertEqual(9, mh.remove())
        self.assertEqual(1, len(mh))
        self.assertEqual(2, mh.peek())

    def test3Elements1(self):
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
        prefix = []
        for x in nums:
            mh.insert(x)
            prefix.append(x)
            s = sorted(prefix)
            self.assertEqual(s[len(s)//2], mh.peek())
        seq = []
        while True:
            try:
                seq.append(mh.remove())
            except IndexError:
                break
        tmp = sorted(nums)
        expected = []
        while tmp:
            m = tmp[len(tmp)//2]
            expected.append(m)
            tmp.pop(len(tmp)//2)
        self.assertEqual(expected, seq)

if __name__ == "__main__":
    unittest.main()