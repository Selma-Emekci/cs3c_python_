"""
CS3C: BinarySearchTree
Copyright 2022 Zibin Yang
(Soft-linked in assignment)
(Do not modify or submit this file for assignments)
"""


class BinaryTreeNode:
    def __init__(self, data, left_child=None, right_child=None):
        self.data = data
        self.left_child = left_child
        self.right_child = right_child

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, data):
        self._data = data

    @property
    def left_child(self):
        return self._left_child

    @left_child.setter
    def left_child(self, left_child):
        self._left_child = left_child

    @property
    def right_child(self):
        return self._right_child

    @right_child.setter
    def right_child(self, right_child):
        self._right_child = right_child

    def __str__(self):
        return str(self.data)

    def __repr__(self):
        return f"data={self.data}, lc={id(self.left_child):#0x}," \
               f" rc={id(self.right_child):#0x}"


class BinarySearchTree:
    class DuplicateDataError(Exception):
        pass

    # TODO: we should be able to merge EmptyTreeError and NotFoundError
    class EmptyTreeError(Exception):
        pass

    class NotFoundError(Exception):
        pass

    def __init__(self, iterable=None):
        # Slight deviation from lecture: takes an optional iterable that
        # contains initial data to populate the tree.
        self._root = None
        self._size = 0
        if iterable:
            for item in iterable:
                self.insert(item)

    # Slight deviation from lecture: make the node used in the tree and
    # class attribute, so subclass (such as AVlTree) may override it
    TreeNode = BinaryTreeNode

    @property
    def size(self):
        return self._size

    def __len__(self):
        return self.size

    def insert(self, data):
        self._root = self._insert(self._root, data)

    def _insert(self, subtree_root, data):
        if subtree_root is None:
            self._size += 1
            return self.TreeNode(data)

        if data == subtree_root.data:
            raise BinarySearchTree.DuplicateDataError(f"data={data} already exists in tree")
        elif data < subtree_root.data:
            subtree_root.left_child = self._insert(subtree_root.left_child, data)
        else:
            subtree_root.right_child = self._insert(subtree_root.right_child, data)

        return subtree_root

    # Slight deviation from lecture: used for both __str__() and __repr__()
    def _str(self, subtree_root, depth, _repr=False):
        if subtree_root is None:
            return ""

        s = ""
        s += self._str(subtree_root.right_child, depth + 1, _repr)
        s += (" " * 4 * depth
              + (repr(subtree_root) if _repr else str(subtree_root))
              + "\n")
        s += self._str(subtree_root.left_child, depth + 1, _repr)
        return s

    def __str__(self):
        return f"size={self.size}\n" + self._str(self._root, 0)

    # Slight deviation from lecture: added __repr__
    def __repr__(self):
        return f"repr: size={self.size}\n" + self._str(self._root, 0, True)

    def __iter__(self):
        return self._iter(self._root)

    def _iter(self, subtree_root):
        if subtree_root is None:
            return

        yield from self._iter(subtree_root.left_child)
        yield subtree_root.data
        yield from self._iter(subtree_root.right_child)

    def find(self, data):
        return self._find_node(data).data

    def _find_node(self, data):
        return self._find_node_recursive(self._root, data)

    def _find_node_recursive(self, subtree_root, data):
        if subtree_root is None:
            raise BinarySearchTree.NotFoundError

        if subtree_root.data == data:
            return subtree_root
        elif data < subtree_root.data:
            return self._find_node_recursive(subtree_root.left_child, data)
        else:
            return self._find_node_recursive(subtree_root.right_child, data)

    def __contains__(self, item):
        try:
            self.find(item)
            return True
        except BinarySearchTree.NotFoundError:
            return False

    def find_min(self):
        return self._find_min(self._root)

    def _find_min(self, subtree_root):
        if subtree_root is None:
            raise BinarySearchTree.EmptyTreeError

        try:
            return self._find_min(subtree_root.left_child)
        except BinarySearchTree.EmptyTreeError:
            return subtree_root.data

    def find_max(self):
        return self._find_max(self._root)

    def _find_max(self, subtree_root):
        if subtree_root is None:
            raise BinarySearchTree.EmptyTreeError

        try:
            return self._find_max(subtree_root.right_child)
        except BinarySearchTree.EmptyTreeError:
            return subtree_root.data

    def remove(self, data):
        self._root = self._remove(self._root, data)

    def _remove(self, subtree_root, data):
        if not subtree_root:
            raise BinarySearchTree.NotFoundError(f"data={data} not found")

        if data < subtree_root.data:
            subtree_root.left_child = self._remove(subtree_root.left_child, data)
        elif subtree_root.data < data:
            subtree_root.right_child = self._remove(subtree_root.right_child, data)
        elif subtree_root.left_child and subtree_root.right_child:
            # node.data == data, so we are at the node that we should remove
            # Find the smallest data on the right, which is guaranteed to be
            # larger than anything on the left, and smaller than anything on
            # the right, and place is in the node
            subtree_root.data = self._find_min(subtree_root.right_child)
            # Now we've duplicated the data, we have to remove it from the
            # right child
            subtree_root.right_child = self._remove(subtree_root.right_child, subtree_root.data)
        else:
            # One (or both) of the children is empty, can just pull the other
            # child up
            subtree_root = subtree_root.left_child if subtree_root.left_child \
                else subtree_root.right_child
            self._size -= 1

        return subtree_root

    # Slight deviation from lecture: added traverse()
    #
    # Optional: you are not required to understand how traverse() works.
    # Making the bst iterable by implementing __iter__() is simpler and
    # a lot more useful than traverse() (see testTraverse())
    def traverse(self, func, initial_result):
        return self._traverse(self._root, func, initial_result)

    def _traverse(self, subtree_root, func, result):
        if subtree_root is None:
            return result

        result = self._traverse(subtree_root.left_child, func, result)
        result = func(result, subtree_root.data)
        result = self._traverse(subtree_root.right_child, func, result)
        return result
