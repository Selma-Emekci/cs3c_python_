"""
CS3C, sorting algorithms
Copyright 2021 Zibin Yang
"""


######################################################################
# Bubble sort
######################################################################
def bubble_sort(iterable):
    def float_largest_to_top(iterable, size):
        swapped = False
        for i in range(size - 1):
            if iterable[i] > iterable[i + 1]:
                iterable[i], iterable[i + 1] = iterable[i + 1], iterable[i]
                swapped = True
        return swapped

    size = len(iterable)
    while float_largest_to_top(iterable, size):
        size -= 1


######################################################################
# Insertion sort, gap of 1
######################################################################
def insertion_sort(iterable):
    for unsorted_index in range(1, len(iterable)):
        unsorted_data = iterable[unsorted_index]
        k = unsorted_index
        while k >= 1 and iterable[k - 1] > unsorted_data:
            iterable[k] = iterable[k - 1]
            k -= 1
        iterable[k] = unsorted_data


######################################################################
# Insertion sort, with gap (this replaces the one above)
######################################################################
def insertion_sort(iterable, gap=1):
    for unsorted_index in range(gap, len(iterable)):
        unsorted_data = iterable[unsorted_index]
        k = unsorted_index
        while k >= gap and iterable[k - gap] > unsorted_data:
            iterable[k] = iterable[k - gap]
            k -= gap
        iterable[k] = unsorted_data


######################################################################
# Shell sort, using insertion sort
######################################################################
def shell_sort(iterable):
    gap = len(iterable) // 2
    while gap > 0:
        insertion_sort(iterable, gap)
        gap //= 2


######################################################################
# Shell sort, with customizable gaps
######################################################################
def shells_gaps(length):
    gap = length // 2
    while gap > 0:
        yield gap
        gap //= 2


def hibbards_gaps(length):
    if length < 2:
        return
    for gap in shells_gaps(length):
        # hibbards is basically shell gap - 1, except when it's 1.
        if gap > 1:
            yield gap - 1
    if gap - 1 != 1:
        yield 1


# Note this replaces the shell_sort() defined above
def shell_sort(iterable, gaps=shells_gaps):
    for gap in gaps(len(iterable)):
        insertion_sort(iterable, gap)


def shell_sort_hibbard(iterable):
    return shell_sort(iterable, gaps=hibbards_gaps)


######################################################################
# Merge sort
######################################################################
def merge_sort(iterable, start=None, end=None):
    def merge(iterable, start1, end1, start2, end2):
        # It's a little complicated to do merge in-place, so this returns
        # a new list with the two iterable
        out = []
        while start1 < end1 and start2 < end2:
            if iterable[start1] < iterable[start2]:
                out.append(iterable[start1])
                start1 += 1
            else:
                out.append(iterable[start2])
                start2 += 1
        out += iterable[start1:end1]
        out += iterable[start2:end2]
        return out

    if start is None:
        start = 0
        end = len(iterable)

    length = end - start
    if length < 2:
        return

    mid = start + length // 2
    merge_sort(iterable, start, mid)
    merge_sort(iterable, mid, end)
    iterable[start:end] = merge(iterable, start, mid, mid, end)
