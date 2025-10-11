"""
CS3C, LinkedList and OrderedLinkedList
Copyright 2025 Zibin Yang (10/9/2025)

Instructor's solution for Assignment 2, Sparse matrix
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
        return f"new_data={self._data}, next={id(self._next)}"


class LinkedList:
    def __init__(self, iterable=None):
        self._head = None
        self._size = 0
        # Added 4/5/21: made it easier to initialize the list
        if iterable is not None:
            iter_ = iter(iterable)
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
        :param data: the new_data to look for in the list
        :return: new_data if it exists in the list
        :raise: KeyError if new_data is not in the list
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

    ### Assignment 2
    def __setitem__(self, index, new_data):
        self._validate_index(index)
        curr = self._head
        while index != 0:
            curr = curr.next
            index -= 1
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

    ### Assignment 2 extra credit, if available
    def __reversed__(self):
        # This uses recursion to reverse the new_data. It technically also holds
        # all new_data in memory because recursion keeps all the stack frames, but
        # doesn't use builtin list/reversed() so it gets full extra credits.
        #
        # A simpler version can just use __getitem__() indexing backwards.
        def reverse_rec(first_node):
            if first_node is None:
                return
            # This is the same as:
            #     yield from reverse_rec(first_node.next)
            # which we haven't covered yet, so using the for loop instead.
            for data in reverse_rec(first_node.next):
                yield data
            yield first_node.data

        return reverse_rec(self._head)


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