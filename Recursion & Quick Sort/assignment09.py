"""
CS3C, Assignment #9, Quick sort recursion limit and pivot selection
Selma Emekci
"""
from quicksort import _partition, _insertion_sort, quick_sort_is
QS_RECURSION_LIMIT = 15
def quick_sort_x(iterable, start=None, end=None, rec_limit=QS_RECURSION_LIMIT):
    """
    rec_limit is the size threshold below which the algorithm switches from
    Quick sort to insertion sort on the current subarray.  It must be at least
    2; otherwise ValueError is raised.  The algorithm sorts iterable in-place
    on the half-open interval [start, end). For tiny rec_limit, insertion sort 
    is used too early and does too much work on larger subarrays.
    """
    if rec_limit < 2:
        raise ValueError("rec_limit must be at least 2")

    if start is None:
        start = 0
        end = len(iterable)

    if start + rec_limit >= end:
        return _insertion_sort(iterable, start, end)

    pivot_index = _partition(iterable, start, end)
    quick_sort_x(iterable, start, pivot_index, rec_limit)
    quick_sort_x(iterable, pivot_index + 1, end, rec_limit)


def quick_sort_my_pivot(iterable, start=None, end=None, rec_limit=QS_RECURSION_LIMIT):
    """
    This function uses the same recursion limit logic and the same _partition() 
    and _insertion_sort() helpers as quick_sort_is(). The only difference is 
    for each recursive call it picks the element in the middle of [start, end) 
    as the pivot, swaps it into position start, and then reuses _partition() unchanged.

    On already-sorted input this middle pivot keeps the partitions roughly
    balanced, so the recursion behaves like the average case and is
    significantly faster than always picking iterable[start] as the pivot.
    """
    if start is None:
        start = 0
        end = len(iterable)

    if start + rec_limit >= end:
        return _insertion_sort(iterable, start, end)

    mid = (start + end - 1) // 2
    iterable[start], iterable[mid] = iterable[mid], iterable[start]

    pivot_index = _partition(iterable, start, end)
    quick_sort_my_pivot(iterable, start, pivot_index, rec_limit)
    quick_sort_my_pivot(iterable, pivot_index + 1, end, rec_limit)


def quick_sort_builtin(iterable):
    """
    The function replaces the contents of iterable with sorted(iterable) so
    that, from the caller's point of view, it behaves like the other *sort()
    functions that sort in-place.  CPython's sorted() uses Timsort, which is
    an adaptive, stable O(n log n) algorithm that exploits existing ordered
    runs in the data.
    """
    iterable[:] = sorted(iterable)
