"""
CS3C, Assignment #1, Subset Sum
Student: Selma Emkci

Implements the subset sum algorithm using both iterative and recursive
approaches (hopefully). 
"""


class Subset:
    """
    Represents a subset of items. Wraps a Python set and keeps a running sum.
    """

    def __init__(self):
        self._items = set()
        self._sum = 0

    def add(self, item):
        """Add item (shallow, reference only)."""
        self._items.add(item)
        self._sum += item  # relies on duck typing / operator overloading

    @property
    def sum(self):
        return self._sum

    def copy(self):
        """Return a shallow copy of this subset."""
        new_subset = Subset()
        new_subset._items = self._items.copy()
        new_subset._sum = self._sum
        return new_subset

    def to_set(self):
        return self._items

    def __eq__(self, other):
        # equality by elements (sum implied)
        return self._items == other._items

    def __str__(self):
        return f"{self._items} (sum={self._sum})"


class Collection:
    """
    Collection of Subset objects.
    """

    def __init__(self):
        empty = Subset()
        self._subsets = [empty]

    def expand_by(self, item, target):
        """
        Expand collection by adding 'item' to each existing subset.
        Skip new subsets whose sum would exceed target.
        """
        new_subsets = []
        for subset in self._subsets:
            new_subset = subset.copy()
            new_subset.add(item)
            if new_subset.sum <= target:
                if new_subset.sum == target:
                    self._subsets.append(new_subset)
                    return new_subset
                new_subsets.append(new_subset)
        self._subsets.extend(new_subsets)
        return None

    @property
    def max_subset(self):
        return max(self._subsets, key=lambda s: s.sum)


def subset_sum(s, target):
    """
    Iterative subset sum algorithm. Returns a Python set of items.
    Raises ValueError if input has duplicates.
    """
    items = list(s)
    if len(items) != len(set(items)):
        raise ValueError("Input contains duplicates")

    col = Collection()
    for x in items:
        result = col.expand_by(x, target)
        if result is not None:
            return result.to_set()
    return col.max_subset.to_set()


def subset_sum_rec(s, target):
    """
    Recursive subset sum algorithm. Returns a Python set of items.
    """
    items = list(s)
    if len(items) != len(set(items)):
        raise ValueError("Input contains duplicates")

    def helper(index, current_set, current_sum):
        if current_sum > target:
            return set(), 0
        if index == len(items):
            return current_set, current_sum

        # Option 1: skip item
        subset1, sum1 = helper(index + 1, current_set.copy(), current_sum)

        # Option 2: include item
        with_item = current_set.copy()
        with_item.add(items[index])
        subset2, sum2 = helper(index + 1, with_item, current_sum + items[index])

        if sum2 > sum1:
            return subset2, sum2
        else:
            return subset1, sum1

    best_subset, _ = helper(0, set(), 0)
    return best_subset


# Extra credit: flexible version
def subset_sum_flex(s, target, value_of=lambda x: x):
    """
    Extra-credit version: allows caller to specify how to compute value
    of each item (e.g., lambda x: x.run_time for iTunesEntry).
    """
    items = list(s)
    if len(items) != len(set(items)):
        raise ValueError("Input contains duplicates")

    col = [set()]  # start with empty set

    for x in items:
        new_subsets = []
        for L in col:
            new_set = set(L)
            new_set.add(x)
            total = sum(value_of(i) for i in new_set)
            if total <= target:
                if total == target:
                    return new_set
                new_subsets.append(new_set)
        col.extend(new_subsets)

    # return the subset with max sum
    return max(col, key=lambda subset: sum(value_of(i) for i in subset))


if __name__ == "__main__":
    # Simple manual tests
    print("subset_sum([] , 10) =", subset_sum([], 10))
    print("subset_sum([5], 10) =", subset_sum([5], 10))
    print("subset_sum([25, 27, 3, 12, 6, 15, 9, 30, 21, 19], 50) =",
          subset_sum([25, 27, 3, 12, 6, 15, 9, 30, 21, 19], 50))
    print("subset_sum_rec([25, 27, 3, 12, 6, 15, 9, 30, 21, 19], 50) =",
          subset_sum_rec([25, 27, 3, 12, 6, 15, 9, 30, 21, 19], 50))
