"""
CS3C, Assignment #3, Timing Matrix Multiplication
Selma Emekci

Implements dense (list-of-lists) and sparse matrix multiplication, plus analysis write-up.
"""

from assignment02 import SparseMatrix, MatrixEntry

def _shape_ll(mat):
    """Return (rows, cols) for a list-of-lists matrix."""
    if not isinstance(mat, (list, tuple)) or len(mat) == 0:
        raise ValueError("Matrix must be a non-empty list of lists.")
    rows = len(mat)
    first_len = None
    for r, row in enumerate(mat):
        if not isinstance(row, (list, tuple)):
            raise ValueError("Row {} is not a list/tuple.".format(r))
        if first_len is None:
            if len(row) == 0:
                raise ValueError("Matrix must have at least 1 column.")
            first_len = len(row)
        elif len(row) != first_len:
            raise ValueError("Matrix rows must all have the same length.")
    return rows, first_len


def _zeros_ll(rows, cols):
    """Allocate a rows x cols list-of-lists with zeros."""
    if rows <= 0 or cols <= 0:
        raise ValueError("Result size must be positive.")
    return [[0 for _ in range(cols)] for _ in range(rows)]


def mulmat(a, b):
    """
    Multiply two matrices a and b (both list-of-lists) and return the product as a new list-of-lists.
    - a is (m x p), b is (p x n) — p must match.
    - Works for rectangular matrices.
    - Raises ValueError on incompatible shapes.

    Big-O (dense, worst-case):
    - Standard triple-loop matrix multiply: O(m * p * n). For square n x n: O(n^3).
    """
    m, p = _shape_ll(a)
    p2, n = _shape_ll(b)
    if p != p2:
        raise ValueError("Incompatible shapes: a is {}x{} and b is {}x{}".format(m, p, p2, n))
    res = _zeros_ll(m, n)
    for i in range(m):
        ai = a[i]
        rij = res[i]
        for k in range(p):
            aik = ai[k]
            if aik == 0:
                continue
            bk = b[k]
            for j in range(n):
                rij[j] += aik * bk[j]
    return res

class SparseMatrixMul(SparseMatrix):
    """
    SparseMatrix subclass that implements matrix multiplication.
    """
    def __init__(self, nrows, ncols):
        super().__init__(nrows, ncols, 0)

    def __matmul__(self, other):
        """
        Multiply self (m x p) with other (p x n) and return result (m x n) as SparseMatrixMul.
        """
        if not isinstance(other, SparseMatrixMul):
            raise TypeError("Right operand must be a SparseMatrixMul")

        m, p = self.nrows, self.ncols
        p2, n = other.nrows, other.ncols
        if p != p2:
            raise ValueError("Incompatible shapes: self is {}x{}, other is {}x{}".format(m, p, p2, n))

        result = SparseMatrixMul(m, n)

        for r in range(m):
            for j in range(n):
                acc = 0
                for entry in self._get_row_list(r):
                    k = entry.column
                    a_rk = entry.value
                    acc += a_rk * other.get(k, j)
                if acc != 0:
                    result.set(r, j, acc)

        return result

    def __matmul_fast__(self, other):
        """
        Extra credit: Multiply using sparsity in BOTH matrices.
        """
        if not isinstance(other, SparseMatrixMul):
            raise TypeError("Right operand must be a SparseMatrixMul")

        m, p = self.nrows, self.ncols
        p2, n = other.nrows, other.ncols
        if p != p2:
            raise ValueError("Incompatible shapes: self is {}x{}, other is {}x{}".format(m, p, p2, n))

        result = SparseMatrixMul(m, n)

        for r in range(m):
            for a_entry in self._get_row_list(r):
                k = a_entry.column
                a_rk = a_entry.value
                for b_entry in other._get_row_list(k):
                    j = b_entry.column
                    b_kj = b_entry.value
                    prev = result.get(r, j)
                    new_val = prev + a_rk * b_kj
                    if new_val != 0:
                        result.set(r, j, new_val)
                    else:
                        result.set(r, j, 0)

        return result


"""
Assignment #3 Analysis

Expectations
Dense mulmat (list-of-lists):
  Let a be (m×p), b be (p×n). Each output cell does p MACs -> Θ(m·p·n).
  Square case (n×n): Θ(n^3).
  MACs -> multiple-accumulate operations

Sparse __matmul__:
  For row r, let nnz_row(r) be non-zeros in self[r]. For each column j of other,
  sum over nnz_row(r) terms via other.get(k, j). Per row cost is Θ(n*nnz_row(r)).
  Summed over all rows is Θ(n*Σ_r nnz_row(r)) = Θ(n*nnz(self)).
  If density d is constant in square case: nnz(self) = d*n^2 -> Θ(d*n^3).

Sparse __matmul_fast__ (extra credit):
  Θ( Σ_{(r,k)∈nnz(self)} nnz(other.row(k)) ) << n·nnz(self) when both are sparse.


Measured timings (seconds)
Dense (mulmat) vs NumPy (square n×n)
  n      mulmat     numpy.matmul
  100    0.0437     0.0007
  200    0.3849     0.0060
  300    1.3355     0.0210
  400    3.3464     0.0599

Sparse (__matmul__) ~1% density (square n×n)
  n      time
  100    0.0235
  200    0.1961
  300    0.7180
  400    1.9353


Growth-rate inference
Dense mulmat (n->2n): ×8.81, ×3.47, ×2.51  = cubic trend (ideal cubic doubles by ×8).
NumPy (n->2n):        ×8.57, ×3.50, ×2.85  = cubic trend
Sparse 1% (n->2n):    ×8.35, ×3.66, ×2.70  = Θ(d·n^3) with d=0.01 constant.

Conclusion/comparison
- Fastest: NumPy, then sparse (when truly sparse), then dense mulmat.
- Dense mulmat is pure-Python triple loop -> large constant + Θ(n^3).
- Sparse __matmul__ matches Θ(n·nnz(self)); with constant density, behaves Θ(d·n^3) and
  outperforms dense when d is small enough. The extra-credit __matmul_fast__ should improve
  more by avoiding zero work in both operands.
"""
