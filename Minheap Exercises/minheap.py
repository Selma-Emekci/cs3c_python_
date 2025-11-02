"""
CS3C Min heap implementation
Copyright 2024 Zibin Yang (5/9/2024)
"""


class MinHeap:
    def __init__(self, initial_data=None):
        if initial_data is None:
            self._heap = [None]
        else:
            # list() turns any iterable into a list, in case initial_data
            # itself is not a list.
            self._heap = [None] + list(initial_data)
            self._order_heap()

    def __len__(self):
        return len(self._heap) - 1

    def __str__(self):
        return f"size={len(self)}, heap={self._heap}"

    def insert(self, data):
        self._heap.append(data)
        self._percolate_up()

    def _percolate_up(self):
        data = self._heap[len(self)]

        child_index = len(self)
        parent_index = child_index // 2  # Typically implemented as bit shift
        while child_index > 1 and data < self._heap[parent_index]:
            self._heap[child_index] = self._heap[parent_index]
            child_index = parent_index
            parent_index = child_index // 2

        self._heap[child_index] = data

    def remove(self):
        if len(self) == 0:
            raise IndexError("Remove from empty min heap")

        return_data = self._heap[1]
        # Always remove data at the end of the heap first
        last_data = self._heap.pop()
        if len(self) > 0:
            self._heap[1] = last_data
            self._percolate_down(1)

        return return_data

    def _percolate_down(self, starting_index):
        # Remember the data at the starting place
        data = self._heap[starting_index]

        while starting_index <= len(self):
            # While we are within the heap
            min_child_index = self._get_min_child_index(starting_index)
            if min_child_index is None:
                # No child, done
                break

            if data > self._heap[min_child_index]:
                # If the parent data is bigger than the smaller child, pull it up
                self._heap[starting_index] = self._heap[min_child_index]
                # Move down to the smaller child
                starting_index = min_child_index
            else:
                # Otherwise, the parent data is smaller already, done
                break

        self._heap[starting_index] = data

    def _get_min_child_index(self, parent_index):
        left_child_index = parent_index * 2  # typically implemented as bit shift
        if left_child_index > len(self):
            # No child
            return None

        right_child_index = left_child_index + 1
        if right_child_index > len(self):
            # No right child, left child is the smaller child
            min_child_index = left_child_index
        elif self._heap[left_child_index] < self._heap[right_child_index]:
            # Have both left and right child, and left child is smaller
            min_child_index = left_child_index
        else:
            # Have  both left child and right child, right child is smaller
            min_child_index = right_child_index

        return min_child_index

    def _order_heap(self):
        # Floyd's method of building the heap
        for i in range(len(self) // 2, 0, -1):
            self._percolate_down(i)

    def peek(self):
        if len(self) == 0:
            raise IndexError("Peeking an empty min heap")

        return self._heap[1]
