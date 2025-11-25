"""
CS3C, sort key function demo
Copyright 2019 Zibin Yang
"""
import copy

from itunes import *


def quick_sort(iterable, start=None, end=None, key=lambda elem: elem):
    def partition(iterable, start, end):
        pivot = iterable[start]
        left, right = start + 1, end - 1
        while True:
            while left <= right and key(iterable[left]) <= key(pivot):
                left += 1
            while left <= right and key(iterable[right]) >= key(pivot):
                right -= 1

            if left > right:
                break

            iterable[left], iterable[right] = iterable[right], iterable[left]

        iterable[start], iterable[right] = iterable[right], iterable[start]

        return right

    if start is None:
        start = 0
        end = len(iterable)

    if start >= end:
        return

    pivot_index = partition(iterable, start, end)

    quick_sort(iterable, start, pivot_index, key)
    quick_sort(iterable, pivot_index + 1, end, key)


if __name__ == '__main__':
    itunes_reader = iTunesEntryReader("itunes_file.txt")
    itunes = [itune for itune in itunes_reader]
    print("*** Original itunes ***")
    print(*itunes, sep="\n")

    itunes_sort_by_run_time = copy.copy(itunes)
    # User-defined type sorting: using a class attribute to sort by time.
    # Two separate lines, and iTunesEntry.sort_by has no obvious relationship
    # to sorting unless the code is examined.
    iTunesEntry.sort_by = iTunesEntry.Sort.TIME
    quick_sort(itunes)
    print("*** Sorted by run time ***")
    print(*itunes_sort_by_run_time, sep="\n")

    itunes_sort_by_run_time = copy.copy(itunes)
    # User-defined type sorting: using a key lambda function to sort by time.
    # One line, and it's explicit that the sorting key is the run_time attribute
    quick_sort(itunes_sort_by_run_time, key=lambda itune: itune.run_time)
    print("*** Sorted by run time ***")
    print(*itunes_sort_by_run_time, sep="\n")
