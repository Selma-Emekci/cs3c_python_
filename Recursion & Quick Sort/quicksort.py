"""
CS3C, quick sort
Copyright 2024 Zibin Yang (5/23/2024)
"""


# Quick sort using extra lists
def quick_sort_el(iterable):
    if len(iterable) < 2:
        return

    small = []
    large = []
    pivot = iterable[0]

    for d in iterable[1:]:
        if d <= pivot:
            small.append(d)
        else:
            large.append(d)

    quick_sort_el(small)
    quick_sort_el(large)
    iterable[::] = small + [pivot] + large


# Quick sort without using extra lists, but examine input elements one
# at a time.
def quick_sort_1e(iterable, start=None, end=None):
    """
    Sort iterable in-place, using the Quick Sort algorithm
    :param iterable: iterable to be sorted, in-place
    :param start: inclusive start index of the iterable to sort
    :param end: exclusive end index of the iterable to sort
    :return: (nothing)
    """
    if start is None:
        start = 0
        end = len(iterable)

    if end - start < 2:
        return

    pivot = iterable[start]

    small, large = start + 1, end - 1
    while small <= large:
        # It's <=, because even with just one element, we need to put it in the
        # smaller/larger half accordingly, so it must go through the comparisons
        if iterable[small] > pivot and iterable[large] < pivot:
            # left is too big, right is too small, both out of place, swap
            iterable[small], iterable[large] = iterable[large], iterable[small]
            small += 1
            large -= 1
        elif iterable[small] < pivot and iterable[large] > pivot:
            # both are in the right place, advance both
            small += 1
            large -= 1
        elif iterable[small] < pivot:
            # left is in the right place, advance
            small += 1
        else:
            # right is in the right place, advance (backwards)
            large -= 1
    iterable[start], iterable[small - 1] = iterable[small - 1], iterable[start]

    quick_sort_1e(iterable, start, small - 1)
    quick_sort_1e(iterable, small, end)


# A slight less smart version that has to explicitly put pivot in the middle.
#
# def quick_sort(iterable, start=None, end=None):
#     """
#     Sort iterable in-place, using the Quick Sort algorithm
#     :param iterable: iterable to be sorted, in-place
#     :param start: inclusive start index of the iterable to sort
#     :param end: exclusive end index of the iterable to sort
#     :return: (nothing)
#     """
#     if start is None:
#         start = 0
#         end = len(iterable)
#
#     if end - start < 2:
#         return
#
#     pivot = iterable[start]
#
#     small, large = start + 1, end - 1
#     while small <= large:
#         # It's <=, because even with just one element, we need to put it in the
#         # smaller/larger half accordingly, so it must go through the comparisons
#         while small <= large and iterable[small] < pivot:
#             # As long as it's not the end and the element is in the right
#             # (smaller) group, keep advancing
#             small += 1
#         while small <= large and iterable[large] > pivot:
#             # As long as it's not the end and the element is in the right
#             # (bigger) group, keep advancing (backward)
#             large -= 1
#         if small < large:
#             # If the two pointers haven't raced passed each other, the elements
#             # they pointers are in the wrong group, so swap them
#             iterable[small], iterable[large] = iterable[large], iterable[small]
#             small += 1
#             large -= 1
#
#     quick_sort(iterable, start + 1, small)
#     quick_sort(iterable, small, end)
#     # Technically these create copies
#     iterable[start:end] = iterable[start + 1:small] + [pivot] + iterable[small:end]


def _partition(iterable, start, end):
    pivot = iterable[start]
    left, right = start + 1, end - 1
    while True:
        while left <= right and iterable[left] <= pivot:
            # As long as the element is in the smaller partition, keep
            # moving forward
            left += 1
        while left <= right and iterable[right] >= pivot:
            # As long as the element is in the bigger partition, keep
            # moving backward
            right -= 1

        # 'right' has gone to the left of 'left', can stop now
        if left > right:
            break

        # If the two pointers haven't raced passed each other, the elements
        # they point to are in the wrong partition, so swap them
        iterable[left], iterable[right] = iterable[right], iterable[left]

    # 'right' is at the end of the smaller partition, swap it with pivot so
    # is in the correct position (everything to its left is smaller, and
    # everything to the right is bigger).
    iterable[start], iterable[right] = iterable[right], iterable[start]

    return right


def quick_sort(iterable, start=None, end=None):
    """
    Sort iterable in-place, using the Quick Sort algorithm.
    :param iterable: iterable to be sorted, in-place
    :param start: inclusive start index of the iterable to sort
    :param end: exclusive end index of the iterable to sort
    :return: (nothing)
    """
    if start is None:
        start = 0
        end = len(iterable)

    if start + 1 >= end:
        # If there's 0 or 1 element in the list, done.
        return

    pivot_index = _partition(iterable, start, end)

    quick_sort(iterable, start, pivot_index)
    quick_sort(iterable, pivot_index + 1, end)


def _insertion_sort(iterable, start=None, end=None):
    if start is None:
        start = 0
        end = len(iterable)
    for unsorted_index in range(start + 1, end):
        unsorted_data = iterable[unsorted_index]
        k = unsorted_index
        while k > start and iterable[k - 1] > unsorted_data:
            iterable[k] = iterable[k - 1]
            k -= 1
        iterable[k] = unsorted_data


def quick_sort_is(iterable, start=None, end=None):
    """
    Sort iterable in-place, using the Quick Sort algorithm; when the
    iterable gets small enough, it'll switch to insertion sort.
    """

    QS_RECURSION_LIMIT = 15

    if start is None:
        start = 0
        end = len(iterable)

    if start + QS_RECURSION_LIMIT >= end:
        return _insertion_sort(iterable, start, end)

    pivot_index = _partition(iterable, start, end)

    quick_sort_is(iterable, start, pivot_index)
    quick_sort_is(iterable, pivot_index + 1, end)


# Quick sort from the readings; it uses media-of-3 as the pivot
def quick_sort_m3(list_to_sort):
    QS_RECURSION_LIMIT = 15

    def _median_three(list_to_sort, left, right):
        center = (left + right) // 2
        if list_to_sort[center] < list_to_sort[left]:
            list_to_sort[left], list_to_sort[center] = \
                list_to_sort[center], list_to_sort[left]

        if list_to_sort[right] < list_to_sort[left]:
            list_to_sort[left], list_to_sort[right] = \
                list_to_sort[right], list_to_sort[left]

        if list_to_sort[right] < list_to_sort[center]:
            list_to_sort[center], list_to_sort[right] = \
                list_to_sort[right], list_to_sort[center]

        list_to_sort[center], list_to_sort[right - 1] = \
            list_to_sort[right - 1], list_to_sort[center]

        return list_to_sort[right - 1]

    def _quick_sort(list_to_sort, left, right):

        if left + QS_RECURSION_LIMIT <= right:
            pivot = _median_three(list_to_sort, left, right)
            i = left
            j = right - 1
            while i < j:
                for i in range(i + 1, j + 1):
                    if pivot <= list_to_sort[i]:
                        break
                for j in range(j - 1, i - 1, -1):
                    if list_to_sort[j] <= pivot:
                        break
                if i < j:
                    list_to_sort[i], list_to_sort[j] = \
                        list_to_sort[j], list_to_sort[i]
                else:
                    break

            list_to_sort[i], list_to_sort[right - 1] = \
                list_to_sort[right - 1], list_to_sort[i]

            _quick_sort(list_to_sort, left, i - 1)
            _quick_sort(list_to_sort, i + 1, right)

        else:
            _insertion_sort_m3(list_to_sort, left, right)

    def _insertion_sort_m3(target, left, right):

        for pos in range(left + 1, right + 1):
            tmp = target[pos]
            k = pos
            while tmp < target[k - 1] and k > 0:
                target[k] = target[k - 1]
                k -= 1
            target[k] = tmp

    _quick_sort(list_to_sort, 0, len(list_to_sort) - 1)
