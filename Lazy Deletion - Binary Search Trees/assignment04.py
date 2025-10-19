"""
CS3C, Assignment #4, Lazy Deletion in Binary Search Trees
Selma Emekci
Implements a lazy-delete BST on top of BinarySearchTree.
"""
from bst import BinarySearchTree, BinaryTreeNode

class LazyBinaryTreeNode(BinaryTreeNode):
    def __init__(self, data, left_child=None, right_child=None, deleted=False):
        super().__init__(data)
        self.left_child = left_child
        self.right_child = right_child
        self._deleted = bool(deleted)

    @property
    def deleted(self) -> bool:
        return self._deleted

    @deleted.setter
    def deleted(self, value: bool):
        self._deleted = bool(value)

    def __str__(self):
        return f"{self.data}(D)" if self.deleted else str(self.data)

    def __repr__(self):
        return (f"{self.__class__.__name__}("
                f"data={repr(self.data)}, "
                f"left_id={id(self.left_child) if self.left_child else None}, "
                f"right_id={id(self.right_child) if self.right_child else None}, "
                f"deleted={self.deleted})")

class LazyBinarySearchTree(BinarySearchTree):
    """BST with lazy deletion."""
    TreeNode = LazyBinaryTreeNode

    def __init__(self, iterable=None):
        super().__init__(iterable=None)
        self._size_physical = 0
        if iterable:
            for x in iterable:
                self.insert(x)

    @property
    def size_physical(self) -> int:
        """# of physical nodes (including soft-deleted)."""
        return self._size_physical

    def _find_node(self, key):
        """Return the node object holding key (ignore deleted flag), else None."""
        cur = self._root
        while cur is not None:
            if key < cur.data:
                cur = cur.left_child
            elif cur.data < key:
                cur = cur.right_child
            else:
                return cur
        return None

    def insert(self, data):
        if self._root is None:
            self._root = self.TreeNode(data)
            self._size += 1
            self._size_physical += 1
            return True

        cur = self._root
        parent = None
        go_left = False

        while cur is not None:
            parent = cur
            if data < cur.data:
                cur = cur.left_child
                go_left = True
            elif cur.data < data:
                cur = cur.right_child
                go_left = False
            else:
                if isinstance(cur, LazyBinaryTreeNode) and cur.deleted:
                    cur.deleted = False
                    self._size += 1
                    return True
                return False
        node = self.TreeNode(data)
        if go_left:
            parent.left_child = node
        else:
            parent.right_child = node
        self._size += 1
        self._size_physical += 1
        return True

    def remove(self, data):
        """
        Soft-delete only
        """
        node = self._find_node(data)
        if node is None or (isinstance(node, LazyBinaryTreeNode) and node.deleted):
            raise BinarySearchTree.NotFoundError
        node.deleted = True
        self._size -= 1

    def find(self, key):
        node = self._find_node(key)
        if node is None or (isinstance(node, LazyBinaryTreeNode) and node.deleted):
            raise BinarySearchTree.NotFoundError
        return node.data

    def find_min(self):
        """
        Return minimal ACTIVE data. Raise EmptyTreeError if no active nodes.
        """
        if self._root is None:
            raise BinarySearchTree.EmptyTreeError

        stack = []
        cur = self._root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.left_child
            node = stack.pop()
            if not getattr(node, "deleted", False):
                return node.data
            cur = node.right_child

        raise BinarySearchTree.EmptyTreeError

    def find_max(self):
        """
        Return maximal ACTIVE data. Raise EmptyTreeError if no active nodes.
        Iterative reverse in-order with early exit.
        """
        if self._root is None:
            raise BinarySearchTree.EmptyTreeError

        stack = []
        cur = self._root
        while stack or cur:
            while cur:
                stack.append(cur)
                cur = cur.right_child
            node = stack.pop()
            if not getattr(node, "deleted", False):
                return node.data
            cur = node.left_child

        raise BinarySearchTree.EmptyTreeError

    def __iter__(self, physical: bool = False):
        """
        In-order traversal
        """
        def walk(n):
            if n is None:
                return
            yield from walk(n.left_child)
            if physical or not getattr(n, "deleted", False):
                yield n.data
            yield from walk(n.right_child)

        return walk(self._root)

    def collect_garbage(self):
        """
        Physically remove all nodes with deleted=True using the base-class remove().
        Logical size remains unchanged
        Physical size decreases by number of deleted nodes.
        """
        saved_size = self._size
        removed_count = 0

        def sweep(node):
            nonlocal removed_count
            if node is None:
                return
            sweep(node.left_child)
            sweep(node.right_child)

            if getattr(node, "deleted", False):
                node.deleted = False
                BinarySearchTree.remove(self, node.data)
                removed_count += 1

        sweep(self._root)
        self._size = saved_size
        self._size_physical -= removed_count

    def __str__(self):
        lines = [f"size={self.size}"]
        lines.append(self._sideways(self._root, 0))
        return "\n".join(lines)

    def __repr__(self):
        active = list(self.__iter__(physical=False))
        physical = list(self.__iter__(physical=True))
        return (f"{self.__class__.__name__}("
                f"size={self.size}, size_physical={self.size_physical}, "
                f"active_inorder={active}, physical_inorder={physical})")

    def _sideways(self, node, depth):
        if node is None:
            return ""
        right = self._sideways(node.right_child, depth + 1)
        me = ("    " * depth) + str(node) + "\n"
        left = self._sideways(node.left_child, depth + 1)
        return right + me + left
