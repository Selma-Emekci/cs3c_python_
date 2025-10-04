"""
CS3C, LinkedList and OrderedLinkedList

Copyright 2022 Zibin Yang

(Use it in SparseMatrix implementation.)
Modified by Selma Emekci
"""


class LinkedListNode:
    def __init__(self, data):
        self.data = data
        self.next = None

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def next(self):
        return self._next

    @next.setter
    def next(self, new_next):
        self._next = new_next

    def __str__(self):
        return f"{self._data}"

    def __repr__(self):
        return f"data={self._data}, next={id(self._next)}"


class LinkedList:
    def __init__(self, iterable=None):
        self._head = None
        self._size = 0
        # Added 4/5/21: made it easier to initialize the list
        if iterable is not None:
            try:
                # Added 4/15/22: Try to reverse it, because we add each
                # element to the head, which would've reversed it.
                iterable = reversed(iterable)
            except TypeError:
                # TypeError means it's not reversible, e.g. a set, so
                # the order doesn't matter, and it's fine to add to head.
                pass
            for i in iterable:
                self.add_to_head(i)

    @property
    def size(self):
        return self._size

    def __len__(self):
        return self.size

    def add_to_head(self, data):
        node = LinkedListNode(data)
        node.next = self._head
        self._head = node
        self._size += 1

    def __iter__(self):
        # https://docs.python.org/3/library/stdtypes.html#generator-types
        # https://docs.python.org/3/tutorial/classes.html#generators
        curr = self._head
        while curr:
            yield curr.data
            curr = curr.next

    def __str__(self):
        # "str(d) for d in self" without surrounding [] makes it a
        # generator expression (that's not yet a full list).
        return " ".join(str(d) for d in self)

    def find(self, data):
        """
        :param data: the data to look for in the list
        :return: data if it exists in the list
        :raise: KeyError if data is not in the list
        """
        for d in self:
            if d == data:
                return d
        raise KeyError(f"{data=} not found")

    def __contains__(self, data):
        try:
            self.find(data)
            return True
        except KeyError:
            return False

    def __getitem__(self, index):
        self._validate_index(index)

        for i, d in enumerate(self):
            if i == index:
                return d

    # Added 10/4/24 by Selma Emekci
    def __setitem__(self, index, new_data):
        """
        Sets the data at the given index to new_data.
        Raises TypeError if index is not an int
               ValueError if index is invalid (negative or out of range)
        """
        self._validate_index(index)

        # Traverse to the node at the given index
        curr = self._head
        for i in range(index):
            curr = curr.next

        # Update
        curr.data = new_data

    def _validate_index(self, index):
        if not isinstance(index, int):
            raise TypeError("index should be int")

        if index < 0 or index >= self.size:
            raise ValueError(f"index {index} is invalid")

    def remove(self, data):
        prev, curr = None, self._head
        while curr:
            if data == curr.data:
                if prev:
                    prev.next = curr.next
                else:
                    self._head = curr.next
                self._size -= 1
                return
            prev, curr = curr, curr.next
        raise KeyError(f"{data=} not found")


class OrderedLinkedList(LinkedList):
    def __init__(self, iterable=None):
        # Added 4/5/21: made it easier to initialize the list
        super().__init__()
        if iterable is not None:
            for i in iterable:
                self.add(i)

    def add(self, data):
        prev, curr = None, self._head

        while curr:
            if data < curr.data:
                break
            prev, curr = curr, curr.next

        node = LinkedListNode(data)
        if prev:
            # This works for insertions both in the middle and at the end
            prev.next = node
        else:
            # prev is None, that means node is self._head
            self._head = node
        node.next = curr

        self._size += 1

    def add_to_head(self, data):
        raise NotImplementedError("Not supported")

    def find(self, data):
        for d in self:
            if d == data:
                return d
            if data < d:
                break
        raise KeyError(f"{data=} not found")
