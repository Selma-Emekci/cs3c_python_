"""
CS3C, Assignment #3, Tests for Timing Matrix Multiplication
Selma Emekci
Tests for mulmat() and SparseMatrixMul using NumPy for validation and timing.
"""

import unittest
import random
import time
import numpy as np

from assignment03 import mulmat, SparseMatrixMul

def dense_from_sparse(sm):
    """Convert a SparseMatrixMul to a list-of-lists dense matrix."""
    return [[sm.get(r, c) for c in range(sm.ncols)] for r in range(sm.nrows)]


def make_random_dense_ll(rows, cols, lo=0, hi=10, rng=None):
    """Return a rows x cols list-of-lists of random ints in [lo, hi)."""
    if rng is None:
        rng = random
    return [[rng.randint(lo, hi - 1) for _ in range(cols)] for _ in range(rows)]


def make_random_sparse(nrows, ncols, density=0.01, lo=0, hi=10, seed=None):
    """
    Build an nrows x ncols SparseMatrixMul with approx. `density` non-zero entries.
    Values are integers in [lo, hi). Default density ~1%.
    """
    if seed is not None:
        random.seed(seed)
    sm = SparseMatrixMul(nrows, ncols)
    target_nnz = max(1, int(nrows * ncols * density))
    used_positions = set()
    while len(used_positions) < target_nnz:
        r = random.randint(0, nrows - 1)
        c = random.randint(0, ncols - 1)
        if (r, c) in used_positions:
            continue
        val = random.randint(lo, hi - 1)
        if val == 0:
            continue
        sm.set(r, c, val)
        used_positions.add((r, c))
    return sm

class TestMulMatDense(unittest.TestCase):
    def test_small_square_manual(self):
        a = [[1, 2],
             [3, 4]]
        b = [[2, 0],
             [1, 2]]
        expected = np.matmul(np.array(a), np.array(b)).tolist()
        result = mulmat(a, b)
        self.assertEqual(result, expected)

    def test_rectangular_2x3_3x2(self):
        a = [[1, 2, 3],
             [4, 5, 6]]
        b = [[7, 8],
             [9, 10],
             [11, 12]]
        expected = np.matmul(np.array(a), np.array(b)).tolist()
        result = mulmat(a, b)
        self.assertEqual(result, expected)

    def test_incompatible_shapes_raises(self):
        a = [[1, 2, 3],
             [4, 5, 6]]
        b = [[1, 2, 3]]
        with self.assertRaises(ValueError):
            mulmat(a, b)

    def test_random_10x10_against_numpy(self):
        rng = random.Random(1234)
        a = make_random_dense_ll(10, 10, lo=0, hi=10, rng=rng)
        b = make_random_dense_ll(10, 10, lo=0, hi=10, rng=rng)
        expected = np.matmul(np.array(a), np.array(b)).tolist()
        result = mulmat(a, b)
        self.assertEqual(result, expected)


class TestSparseMatrixMul(unittest.TestCase):
    def test_small_square_manual(self):
        sm1 = SparseMatrixMul(2, 2)
        sm2 = SparseMatrixMul(2, 2)
        sm1.set(0, 0, 1)
        sm1.set(0, 1, 2)
        sm1.set(1, 0, 3)
        sm1.set(1, 1, 4)

        sm2.set(0, 0, 2)
        sm2.set(1, 0, 1)
        sm2.set(1, 1, 2)

        result = sm1 @ sm2
        a = [[1, 2],
             [3, 4]]
        b = [[2, 0],
             [1, 2]]
        expected = np.matmul(np.array(a), np.array(b)).tolist()
        result_ll = dense_from_sparse(result)
        self.assertEqual(result_ll, expected)

    def test_rectangular_2x3_3x2(self):
        sm1 = SparseMatrixMul(2, 3)
        sm2 = SparseMatrixMul(3, 2)

        sm1.set(0, 0, 1)
        sm1.set(0, 1, 2)
        sm1.set(0, 2, 3)
        sm1.set(1, 0, 4)
        sm1.set(1, 1, 5)
        sm1.set(1, 2, 6)

        sm2.set(0, 0, 7)
        sm2.set(0, 1, 8)
        sm2.set(1, 0, 9)
        sm2.set(1, 1, 10)
        sm2.set(2, 0, 11)
        sm2.set(2, 1, 12)

        result = sm1 @ sm2
        a = [[1, 2, 3],
             [4, 5, 6]]
        b = [[7, 8],
             [9, 10],
             [11, 12]]
        expected = np.matmul(np.array(a), np.array(b)).tolist()
        self.assertEqual(dense_from_sparse(result), expected)

    def test_incompatible_shapes_raises(self):
        sm1 = SparseMatrixMul(2, 3)
        sm2 = SparseMatrixMul(4, 2)
        with self.assertRaises(ValueError):
            _ = sm1 @ sm2

    def test_wrong_type_raises(self):
        sm1 = SparseMatrixMul(2, 2)
        with self.assertRaises(TypeError):
            _ = sm1 @ [[1, 2], [3, 4]]
    
    def test_random_10x10_against_numpy(self):
        n = 10
        sm1 = make_random_sparse(n, n, density=0.10, lo=0, hi=10, seed=777)
        sm2 = make_random_sparse(n, n, density=0.10, lo=0, hi=10, seed=999)
        result = sm1 @ sm2
        a = np.array(dense_from_sparse(sm1))
        b = np.array(dense_from_sparse(sm2))
        expected = np.matmul(a, b).tolist()
        self.assertEqual(dense_from_sparse(result), expected)

def time_function(label, func, *args, repeats=1):
    """Time a function."""
    best = None
    for _ in range(repeats):
        t0 = time.perf_counter()
        func(*args)
        t1 = time.perf_counter()
        elapsed = t1 - t0
        if best is None or elapsed < best:
            best = elapsed
    print("{:<24} {:>8.4f} s".format(label, best))
    return best


def run_performance_suite():
    """
    Measure and print timings of:
      - mulmat (dense list-of-lists)
      - numpy.matmul
      - SparseMatrixMul.__matmul__ (with ~1% density)
    Sizes are square n x n.
    """
    print("\nDense (mulmat) vs NumPy")
    sizes = [100, 200, 300, 400]
    rng = random.Random(2025)

    for n in sizes:
        a = make_random_dense_ll(n, n, lo=0, hi=10, rng=rng)
        b = make_random_dense_ll(n, n, lo=0, hi=10, rng=rng)
        arr_a = np.array(a)
        arr_b = np.array(b)

        print("\nSize: {} x {}".format(n, n))
        t_mulmat = time_function("mulmat", mulmat, a, b, repeats=1)
        t_numpy = time_function("numpy.matmul", np.matmul, arr_a, arr_b, repeats=3)

    print("\nSparse (__matmul__) ~1% density")
    sizes_sparse = [100, 200, 300, 400]
    for n in sizes_sparse:
        sm1 = make_random_sparse(n, n, density=0.01, lo=0, hi=10, seed=123)
        sm2 = make_random_sparse(n, n, density=0.01, lo=0, hi=10, seed=456)

        print("\nSize: {} x {} (sparse ~1%)".format(n, n))
        time_function("Sparse __matmul__", lambda x, y: x @ y, sm1, sm2, repeats=1)


if __name__ == "__main__":
    random.seed(42)
    np.random.seed(42)
    run_performance_suite()
    unittest.main()
