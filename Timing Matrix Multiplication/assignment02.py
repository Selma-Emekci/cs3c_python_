"""
CS3C, Assignment #2, Sparse matrix
Copyright 2025 Zibin Yang (10/9/2025)
Instructor's solution
"""

from functools import total_ordering
from linkedlist import *
from linkedlist import OrderedLinkedList


@total_ordering
class MatrixEntry:
    """An instance of this class represent a cell in the SparseMatrix."""

    def __init__(self, column, value):
        self._column = column
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = value

    @property
    def column(self):
        return self._column

    def __eq__(self, other):
        if isinstance(other, MatrixEntry):
            return self.column == other.column
        else:
            # Assume other is a column number.
            # This is useful, for example, when SparseMatrix.get()
            # does a .find(c) where c is a column number rather MatrixEntry.
            return self.column == other

    def __lt__(self, other):
        if isinstance(other, MatrixEntry):
            return self.column < other.column
        else:
            # Assume other is a column number, as above. Useful for
            # OrderedLinkedList.
            return self.column < other


class SparseMatrix:
    """
    This represent a sparse matrix that has a default value. If a cell's
    value is not explicitly set, it's assume to contain the default value.
    """

    def __init__(self, nrows, ncols, default_value):
        # All these are read-only properties that cannot be changed once
        # initialized.
        if nrows <= 0:
            raise ValueError(f"nrows should be positive")
        if ncols <= 0:
            raise ValueError(f"ncols should be positive")

        self._nrows = nrows
        self._ncols = ncols
        self._default_value = default_value
        # Call clear() to initialize the top-leve list
        self.clear()

    @property
    def nrows(self):
        return self._nrows

    @property
    def ncols(self):
        return self._ncols

    @property
    def default_value(self):
        return self._default_value

    def clear(self):
        # We can possibly initialize everything to None, and allocate
        # OrderedLinkedList() in set() as needed.
        self._rows = [OrderedLinkedList() for _ in range(self.nrows)]

    def _validate_row_col(self, row, col):
        if row < 0 or row >= self.nrows:
            raise IndexError(f"r={row} is invalid")
        if col < 0 or col >= self.ncols:
            raise IndexError(f"c={col} is invalid")

    def get(self, row, col):
        """Returns value at row, col"""
        self._validate_row_col(row, col)

        try:
            # .new_data is MatrixEntry, .value is what's stored in the MatrixEntry
            return self._rows[row].find(col).value
        except KeyError:
            return self.default_value

    def set(self, row, col, value):
        """Set value at row, col"""
        self._validate_row_col(row, col)

        row = self._rows[row]
        if value == self.default_value:
            # If setting to default value, try to remove the existing entry.
            try:
                row.remove(col)
            except KeyError:
                # There may not be an existing entry, and that's ok.
                pass
            return

        try:
            # If there's an existing value at column, update its value.
            row.find(col).value = value
        except KeyError:
            # Otherwise, add a new entry for the new value.
            row.add(MatrixEntry(col, value))

    def get_row(self, row):
        """Returns a generator that yields all values at row"""

        # This generator is written as a nested function; it can be written
        # as an instance method if one is not familiar with nested function.
        def row_iter():
            # This version walks the linked list of the row just once.
            column, row_list_iter = 0, iter(self._get_row_list(row))
            matrix_entry = next(row_list_iter, None)
            while column < self.ncols:
                if matrix_entry is None or column < matrix_entry.column:
                    # If there's no matrix entry, or we are in-between entries,
                    # just yield the default value.
                    yield self.default_value
                else:
                    # Otherwise, we've reached an entry with non-default value.
                    yield matrix_entry.value
                    matrix_entry = next(row_list_iter, None)
                column += 1

        # get_row() itself cannot contain yield, which would turn it into a
        # generator that's not executed until next() is called on it, and
        # as result doesn't satisfy the requirement of immediately raising
        # exception for invalid index.
        self._validate_row_col(row, 0)
        return row_iter()

    def get_col(self, col):
        """Returns a generator that yields all values at column"""
        self._validate_row_col(0, col)
        # This uses generator expression.
        return (self.get(row, col) for row in range(self.nrows))

    # This is useful for tests to object the list that represents row
    # and do related tests.
    def _get_row_list(self, row):
        return self._rows[row]

    # This version of __str__() uses nested str.join() and doesn't support
    # partial matrix (which is ok given the current assignment requirement).
    def __str__(self):
        return "\n".join((" ".join(str(self.get(r, c)) for c in range(self.ncols)))
                         for r in range(self.nrows))

    ### Depending on the assignment requirements, partial matrix (__str__()
    ### with parameters) with clipping may not be necessary.

    ### This implementation clips the row/column at the boundaries before
    ### iterating through them, so it's a little faster.
    def __str_partial_matrix__(self, starting_row=None, starting_col=None, nrows=None, ncols=None):
        if starting_row is None:
            starting_row = 0
        if starting_col is None:
            starting_col = 0
        if nrows is None:
            nrows = self.nrows
        if ncols is None:
            ncols = self.ncols

        if nrows < 0 or ncols < 0:
            raise ValueError("nrows or ncols should not be negative")

        # clip them
        rstart = max(starting_row, 0)
        cstart = max(starting_col, 0)
        rend = min(self.nrows, starting_row + nrows)
        cend = min(self.ncols, starting_col + ncols)

        s = ""

        for r in range(rstart, rend):
            for c in range(cstart, cend):
                s += str(self.get(r, c)) + " "
            s += "\n"

        return s


if __name__ == '__main__':
    sm = SparseMatrix(2, 3, -1)  # Allocate a 2x3 sparse matrix with default value -1
    print(f"original sm:\n{sm}")  # Print the whole matrix
    print(f"{len(sm._get_row_list(0))=}")  # Row 0's linked list should have nothing
    sm.set(0, 1, 100)  # Set row 0 column 1 to 100
    print(f"sm:\n{sm}")  # Print the whole matrix
    print(f"{len(sm._get_row_list(0))=}")  # Row 0's linked list should have 1 entry
    try:
        sm.get_row(10)  # This should immediately raise IndexError
        print("get_row() incorrectly did not raise IndexError")
    except IndexError:
        print("get_row() correctly and immediately raises IndexError")
    print("row 0: ", list(sm.get_row(0)))  # Print list of values in row 0
    print("col 1: ", list(sm.get_col(1)))  # Print list of values in column 1