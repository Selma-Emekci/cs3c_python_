"""
CS3C, Assignment #2, Sparse Matrices
Selma Emekci
A sparse matrix implemented with OrderedLinkedList rows to the best of my ability.
"""
from linkedlist import OrderedLinkedList

class MatrixEntry:
    """
    Represents one non-default cell in a sparse matrix row.
    """
    def __init__(self, col, value):
        self.col = col
        self.value = value

    def __lt__(self, other):
        if not isinstance(other, MatrixEntry):
            return NotImplemented
        return self.col < other.col

    def __eq__(self, other):
        if not isinstance(other, MatrixEntry):
            return False
        return self.col == other.col

    def __repr__(self):
        return f"MatrixEntry(col={self.col}, value={self.value})"


class SparseMatrix:
    """
    Sparse matrix using an OrderedLinkedList for each row.
    """

    def __init__(self, nrows, ncols, default_value):
        """
        Initialize a sparse matrix.
        :param nrows: number of rows (> 0)
        :param ncols: number of columns (> 0)
        :param default_value: default value for all cells not explicitly set
        """
        if nrows <= 0 or ncols <= 0:
            raise ValueError("Matrix dimensions must be positive.")

        self._nrows = nrows
        self._ncols = ncols
        self._default = default_value
        self._rows = [OrderedLinkedList() for _ in range(nrows)]
        self.clear()
    
    def _validate_row(self, row):
        if not isinstance(row, int) or row < 0 or row >= self._nrows:
            raise IndexError("Row index out of range.")

    def _validate_col(self, col):
        if not isinstance(col, int) or col < 0 or col >= self._ncols:
            raise IndexError("Column index out of range.")

    def _entry_probe(self, col):
        return MatrixEntry(col, None)

    def clear(self):
        """Remove all non-default entries from the matrix."""
        self._rows = [OrderedLinkedList() for _ in range(self._nrows)]

    def get(self, row, col):
        """
        Return the value at (row, col). Raises IndexError for invalid indices.
        Returns the default value if the entry is not present.
        """
        self._validate_row(row)
        self._validate_col(col)

        row_list = self._rows[row]
        try:
            entry = row_list.find(self._entry_probe(col))
            return entry.value
        except KeyError:
            return self._default

    def set(self, row, col, new_value):
        """
        Set the value at (row, col). Raises IndexError for invalid indices.
        - If new_value == default, remove the entry if it exists; otherwise no-op.
        """
        self._validate_row(row)
        self._validate_col(col)

        row_list = self._rows[row]
        probe = self._entry_probe(col)

        if new_value == self._default:
            try:
                row_list.remove(probe)
            except KeyError:
                pass
            return

        try:
            entry = row_list.find(probe)
            entry.value = new_value
        except KeyError:
            row_list.add(MatrixEntry(col, new_value))

    def get_row(self, row):
        """
        Yield all values in the given row (in column order) as a generator.
        """
        self._validate_row(row)
        row_list = self._rows[row]

        prev_col = -1
        for entry in row_list:
            gap = entry.col - prev_col - 1
            for _ in range(gap):
                yield self._default
            yield entry.value
            prev_col = entry.col

        # trailing defaults to the end of the row
        for _ in range(self._ncols - prev_col - 1):
            yield self._default

    def get_col(self, col):
        """
        Yield all values in the given column (top to bottom) as a generator.
        """
        self._validate_col(col)
        for r in range(self._nrows):
            yield self.get(r, col)

    def _get_row_list(self, row):
        """
        Return the row's OrderedLinkedList.
        """
        return self._rows[row]

    def __str__(self):
        """Return a rectangular string representation of the matrix."""
        lines = []
        for r in range(self._nrows):
            line = " ".join(str(v) for v in self.get_row(r))
            lines.append(line)
        return "\n".join(lines)
