"""
CS3C, Assignment #6, Min-heap exercises (InstrumentedMinHeap + MedianHeap)
<your name here>

This module provides:
- InstrumentedMinHeap: a subclass of MinHeap that counts percolation data
  movements for performance experiments (extra credit).
- MedianHeap: a heap-like ADT that returns the median on peek()/remove(),
  implemented using only MinHeap internally and preserving O(log n) ops.

Notes:
- We rely ONLY on MinHeap (provided) for heap behavior; no Python sorting or
  dicts that would change asymptotics.
"""

from typing import Iterable, Optional
import time
from minheap import MinHeap  # provided by the course


# -------------------------------
# Problem 2 helper (extra credit)
# -------------------------------

class InstrumentedMinHeap(MinHeap):
    """
    A MinHeap that counts *data movements* during percolation.

    "Data movements" means assignments into self._heap[k] (i.e., when a value is
    written into a slot during percolate-up or percolate-down, including the
    final placement). This lets us compare William's (insert repeatedly) vs
    Floyd's (heapify) methods by counting the fundamental work.

    Attributes:
        up_moves (int): movements performed inside _percolate_up()
        down_moves (int): movements performed inside _percolate_down()
    """
    def __init__(self, initial_data: Optional[Iterable]=None):
        self.up_moves = 0
        self.down_moves = 0
        super().__init__(initial_data)

    # Override the two percolation helpers and increment counters where we write.
    def _percolate_up(self):
        data = self._heap[len(self)]

        child_index = len(self)
        parent_index = child_index // 2
        while child_index > 1 and data < self._heap[parent_index]:
            # shift parent down into child slot
            self._heap[child_index] = self._heap[parent_index]
            self.up_moves += 1
            child_index = parent_index
            parent_index = child_index // 2

        # final placement of data
        self._heap[child_index] = data
        self.up_moves += 1

    def _percolate_down(self, starting_index):
        data = self._heap[starting_index]

        while starting_index <= len(self):
            min_child_index = self._get_min_child_index(starting_index)
            if min_child_index is None:
                break

            if data > self._heap[min_child_index]:
                # pull child up into parent slot
                self._heap[starting_index] = self._heap[min_child_index]
                self.down_moves += 1
                starting_index = min_child_index
            else:
                break

        # final placement of data
        self._heap[starting_index] = data
        self.down_moves += 1


# -----------------------------------
# Problem 3: MedianHeap (main task)
# -----------------------------------

class _MaxHeapViaMinHeap:
    """
    A small adapter that implements a max-heap interface using the provided
    MinHeap by storing negated numbers. We assume numeric inputs (per assignment
    examples). Only the methods we need are implemented.

    All methods are O(log n) except len which is O(1), as they delegate to MinHeap.
    """
    def __init__(self):
        self._h = MinHeap()

    def __len__(self):
        return len(self._h)

    def insert(self, x):
        self._h.insert(-x)

    def peek(self):
        return -self._h.peek()

    def remove(self):
        return -self._h.remove()


class MedianHeap:
    """
    A heap-like ADT that supports O(log n) insert/remove and O(1) peek, where
    the "top" is the **median** under the assignment’s definition:
      median index = len(sorted_list) // 2  (upper median for even-sized lists)

    Design & invariants:
    - Uses ONLY the provided MinHeap:
        * upper: MinHeap for the upper half (all elements >= median)
        * lower: max-heap implemented via MinHeap by negation (_MaxHeapViaMinHeap)
    - Invariant: all(x in lower) <= all(y in upper)
    - Size invariant: len(upper) == len(lower) or len(upper) == len(lower) + 1
        This guarantees that the median (as defined) is upper.peek().
    - peek(): O(1) -> return upper.peek()
    - remove(): O(log n) -> remove and return upper.remove(); then rebalance
    - insert(): O(log n) -> insert into one side; then rebalance
    - __init__(initial_data): inserts items individually (allowed O(n log n))

    Why the size invariant?
    For n items, the required median is the element at index n//2 (0-based).
      - If n is odd, n//2 belongs to the upper half (upper has one more).
      - If n is even, n//2 is the first element of the upper half (upper and
        lower have equal sizes). So the median is min of upper, i.e., upper.peek().
    """

    def __init__(self, initial_data: Optional[Iterable]=None):
        self._upper = MinHeap()              # min-heap: holds >= median
        self._lower = _MaxHeapViaMinHeap()   # max-heap via min-heap: holds <= median

        if initial_data is not None:
            for x in initial_data:
                self.insert(x)

    def __len__(self):
        return len(self._upper) + len(self._lower)

    def __str__(self):
        return (f"size={len(self)}, "
                f"upper_size={len(self._upper)}, lower_size={len(self._lower)}")

    # ---- core ops ----

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peeking an empty median heap")
        return self._upper.peek()

    def insert(self, x):
        # Decide destination
        if len(self._upper) == 0 or x >= self._upper.peek():
            self._upper.insert(x)
        else:
            self._lower.insert(x)
        # Rebalance to keep size invariant
        self._rebalance_after_insert()

    def remove(self):
        if len(self) == 0:
            raise IndexError("Remove from empty median heap")
        # Median is always the root of upper
        median = self._upper.remove()
        # Rebalance to keep invariant after removal
        self._rebalance_after_remove()
        return median

    # ---- helpers ----

    def _rebalance_after_insert(self):
        # upper can be either equal to lower, or one bigger
        if len(self._upper) < len(self._lower):
            # move max from lower to upper
            self._upper.insert(self._lower.remove())
        elif len(self._upper) > len(self._lower) + 1:
            # move min from upper to lower
            self._lower.insert(self._upper.remove())

    def _rebalance_after_remove(self):
        if len(self._upper) < len(self._lower):
            self._upper.insert(self._lower.remove())
        # If upper is > lower + 1 here, something else is off; normal flow won’t hit it.
