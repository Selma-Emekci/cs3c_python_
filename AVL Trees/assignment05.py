"""
CS3C, Assignment #5, AVL Tree
Selma Emekci
AVL implementation with single/double rotations and rebalancing on remove
"""
from bst import BinarySearchTree, BinaryTreeNode
class AvlTreeNode(BinaryTreeNode):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.height = 0

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        self._height = value

    def __repr__(self):
        return super().__repr__() + f", height={self.height}"

    @property
    def child_heights(self):
        left_h = self.left_child.height if self.left_child else -1
        right_h = self.right_child.height if self.right_child else -1
        return left_h, right_h

    def adjust_height(self):
        lh, rh = self.child_heights
        self.height = 1 + (lh if lh > rh else rh)

class AvlTree(BinarySearchTree):
    """AVL tree on BinarySearchTree with node heights and rotations."""
    TreeNode = AvlTreeNode
    @property
    def height(self):
        return self._root.height if self._root else -1

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

        subtree_root.adjust_height()
        return self._rotate(subtree_root)

    def _remove(self, subtree_root, data):
        if subtree_root is None:
            raise BinarySearchTree.NotFoundError(f"data={data} not found")

        if data < subtree_root.data:
            subtree_root.left_child = self._remove(subtree_root.left_child, data)
        elif subtree_root.data < data:
            subtree_root.right_child = self._remove(subtree_root.right_child, data)
        else:
            if subtree_root.left_child and subtree_root.right_child:
                min_on_right = self._find_min_node(subtree_root.right_child)
                subtree_root.data = min_on_right.data
                subtree_root.right_child = self._remove(subtree_root.right_child, min_on_right.data)
            else:
                replacement = subtree_root.left_child if subtree_root.left_child else subtree_root.right_child
                self._size -= 1
                return replacement
        subtree_root.adjust_height()
        return self._rotate(subtree_root)

    def _find_min_node(self, subtree_root):
        curr = subtree_root
        while curr and curr.left_child:
            curr = curr.left_child
        return curr

    def _rotate_left(self, subtree_root):
        """Single left rotation (RR case)"""
        rc = subtree_root.right_child
        subtree_root.right_child = rc.left_child
        rc.left_child = subtree_root
        subtree_root.adjust_height()
        rc.adjust_height()
        return rc

    def _rotate_right(self, subtree_root):
        """Single right rotation (LL case)"""
        lc = subtree_root.left_child
        subtree_root.left_child = lc.right_child
        lc.right_child = subtree_root
        subtree_root.adjust_height()
        lc.adjust_height()
        return lc

    def _rotate(self, subtree_root):
        """Detect imbalance and apply single/double rotations & return new subtree root."""
        lh, rh = subtree_root.child_heights
        balance = lh - rh
        if balance > 1:
            llh, lrh = subtree_root.left_child.child_heights
            if llh >= lrh:
                return self._rotate_right(subtree_root)
            else:
                subtree_root.left_child = self._rotate_left(subtree_root.left_child)
                return self._rotate_right(subtree_root)
        if balance < -1:
            rl_h, rr_h = subtree_root.right_child.child_heights
            if rr_h >= rl_h:
                # RR case
                return self._rotate_left(subtree_root)
            else:
                # RL case
                subtree_root.right_child = self._rotate_right(subtree_root.right_child)
                return self._rotate_left(subtree_root)
        return subtree_root
