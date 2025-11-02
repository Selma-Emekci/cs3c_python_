"""
CS3C, Assignment #6, Min-heap exercises
Selma Emekci
Implementation of Instrmented MinHeap and MedianHeap
"""
from typing import Iterable, Optional
from minheap import MinHeap

class InstrumentedMinHeap(MinHeap):
    """
    A MinHeap that counts data movements during percolation.
    """
    def __init__(self, initial_data: Optional[Iterable] = None):
        self.up_moves = 0
        self.down_moves = 0
        super().__init__(initial_data)

    def _percolate_up(self):
        data = self._heap[len(self)]
        child_index = len(self)
        parent_index = child_index // 2
        while child_index > 1 and data < self._heap[parent_index]:
            self._heap[child_index] = self._heap[parent_index]
            self.up_moves += 1
            child_index = parent_index
            parent_index = child_index // 2
        self._heap[child_index] = data
        self.up_moves += 1

    def _percolate_down(self, starting_index):
        data = self._heap[starting_index]

        while starting_index <= len(self):
            min_child_index = self._get_min_child_index(starting_index)
            if min_child_index is None:
                break

            if data > self._heap[min_child_index]:
                self._heap[starting_index] = self._heap[min_child_index]
                self.down_moves += 1
                starting_index = min_child_index
            else:
                break
        self._heap[starting_index] = data
        self.down_moves += 1


class _MaxHeapViaMinHeap:
    """
    All methods are O(log n) except len which is O(1).
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
    the top is the median
    """
    def __init__(self, initial_data: Optional[Iterable] = None):
        self._upper = MinHeap()
        self._lower = _MaxHeapViaMinHeap()

        if initial_data is not None:
            for x in initial_data:
                self.insert(x)

    def __len__(self):
        return len(self._upper) + len(self._lower)

    def __str__(self):
        return (f"size={len(self)}, "
                f"upper_size={len(self._upper)}, lower_size={len(self._lower)}")

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peeking an empty median heap")
        return self._upper.peek()

    def insert(self, x):
        if len(self._upper) == 0 or x >= self._upper.peek():
            self._upper.insert(x)
        else:
            self._lower.insert(x)
        self._rebalance_after_insert()

    def remove(self):
        if len(self) == 0:
            raise IndexError("Remove from empty median heap")
        median = self._upper.remove()
        self._rebalance_after_remove()
        return median

    def _rebalance_after_insert(self):
        if len(self._upper) < len(self._lower):
            self._upper.insert(self._lower.remove())
        elif len(self._upper) > len(self._lower) + 1:
            self._lower.insert(self._upper.remove())

    def _rebalance_after_remove(self):
        if len(self._upper) < len(self._lower):
            self._upper.insert(self._lower.remove())
