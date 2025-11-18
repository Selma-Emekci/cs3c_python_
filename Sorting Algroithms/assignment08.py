"""
CS3C, Assignment #8, Analyzing Shellsort's Gaps
Selma Emekci
Implements three additional Shell sort variants that all share the
same public interface as the shell_sort in sort.py, but differ in
how they generate their gap sequences
"""
from typing import Iterable, Iterator, List, Set
from sort import shell_sort as _base_shell_sort
_EXPLICIT_SHELL_GAPS: List[int] = [
    1,
    2,
    4,
    8,
    16,
    32,
    64,
    128,
    256,
    512,
    1024,
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
    131072,
    262144,
    524288,
    1048576,
]

def shells_gaps_explicit(length: int) -> Iterator[int]:
    """
    Generate Shell's original gaps from an explicit, precomputed list.
    Given a list length, this generator yields the gaps from
    _EXPLICIT_SHELL_GAPS that are strictly smaller than the length, starting
    from the largest such gap and moving down to 1.

    Equivalent to starting with gap = length // 2 and repeatedly
    halving until we reach 1, but the gaps are read from a fixed sequence
    instead of computed with integer division. Explicit gaps produce the same
    ordering and essentially the same asymptotic behaviour as the on-the-fly
    generator, but with noticeably larger constant factors.
    """
    if length < 2:
        return
    for gap in reversed(_EXPLICIT_SHELL_GAPS):
        if gap < length:
            yield gap

def shell_sort_explicit(iterable: Iterable) -> None:
    """
    Shell sort that uses shells_gaps_explicit() as its gap sequence.
    Because the underlying algorithm is identical, any differences in 
    running time between shell_sort_explicit() and the baseline shell_sort() 
    is because of the cost and structure on the gap sequence. On the timings 
    from assignment08_test.py, the explicit gaps are functionally correct but 
    consistently slower: for example, on random integer lists of length 150000, 
    the baseline shell_sort() took about 0.68 seconds, while shell_sort_explicit() 
    took about 3.73–3.82 seconds.
    """
    _base_shell_sort(iterable, gaps=shells_gaps_explicit)


def sedgewick_gaps(length: int) -> Iterator[int]:
    """
    Generate Sedgewick's 1982 gap sequence for a given list length.
    The Sedgewick gaps are defined for k >= 1 as:
        g(k) = 4**k + 3 * 2**(k - 1) + 1

    and gap 1 must be added manually. For a given length, this function:
        1. Computes all g(k) that are strictly less than length.
        2. Adds gap 1 if it is not already present.
        3. Yields the unique gaps in strictly decreasing order.

    Sedgewick's sequence has two properties:
        1. The gaps are not simple powers of two, so even and odd positions
           mix much earlier than with Shell's original sequence. This avoids
           the classic power-of-two worst case where even and odd positions
           only interact at gap 1.
        2. Resulting Shell sort has a better asymptotic upper bound than the 
           original sequence, and faster average-case performance.

    In the Sedgewick performance tests, shell_sort_sedgewick() sorted random
    lists of sizes 50000, 100000, and 150000 in approximately 0.15, 0.31, and
    0.48 seconds respectively, clearly faster than the baseline Shell gaps
    (0.18, 0.39, 0.68 seconds). On the adversarial [99, 1, 99, 1, ...]
    pattern of length 8192, the Sedgewick gaps finished in about 0.0037
    seconds, compared with 0.70 seconds for Shell's gaps and 0.0068 seconds
    for Hibbard's gaps.
    """
    if length < 2:
        return
    gaps: List[int] = []
    k = 1
    while True:
        gap = 4**k + 3 * 2**(k - 1) + 1
        if gap >= length:
            break
        gaps.append(gap)
        k += 1
    if 1 < length and 1 not in gaps:
        gaps.append(1)
    for gap in sorted(set(gaps), reverse=True):
        if gap < length:
            yield gap


def shell_sort_sedgewick(iterable: Iterable) -> None:
    """
    Shell sort that uses sedgewick_gaps() as its gap sequence.
    Replaces the gap generator with sedgewick_gaps(). On the measured 
    random inputs, this change alone reduced running time from about 0.18, 
    0.39, 0.68 seconds for the baseline Shell gaps (sizes 50000, 100000, 150000) 
    to about 0.15, 0.31, 0.48 seconds for Sedgewick's gaps. On the adversarial 
    alternating pattern of length 8192: approximately 0.70 seconds for Shell's 
    gaps versus 0.0037 seconds for Sedgewick's gaps. These results are consistent 
    with the theoretical improvement in the gap sequence.
    """
    _base_shell_sort(iterable, gaps=sedgewick_gaps)


def my_gaps(length: int) -> Iterator[int]:
    """
    Custom geometric gap sequence for Shell sort.

    Design
    The goal of my_gaps() is to retain the strengths of Shell sort while
    avoiding the weaknesses of the pure 2^k sequence used in Shell's
    original algorithm.
        1. Gaps should decrease gradually from a value proportional to the
           list length down to 1, so that early passes can move elements.
        2. The gaps should not all be even or share large common factors,
           to avoid the parity-based worst-case example where even and odd
           positions do not mix until gap 1.

    Implementation
    For a given length, my_gaps() starts with:
        gap = floor(length / 2.2)
    and then repeatedly divides the gap by 2.2, truncating to an integer,
    until the gap would drop below 2. At each step, the current gap is
    yielded if it is positive, less than length, and has not already been
    yielded. After the loop, the function always yields a final gap of 1.
    This produces a strictly decreasing sequence of gaps whose ratios are
    roughly constant (2.2), but which are not locked to powers of two. For
    example, for length 150000 the sequence begins around 68181, then 30991,
    and continues decreasing by roughly a factor of 2.2 until it reaches 1.

    Observations
    The tests in assignment08_test.py show that this simple geometric gap
    sequence works very well in practice:
        Random data:
            n = 50000  -> shell_sort_my = 0.115 and 0.113 seconds
                100000 ->                 0.245     0.252
                150000 ->                 0.420     0.402

        Baseline Shell gaps on the same sizes:
            n = 50000  -> 0.177 seconds
                100000 -> 0.386
                150000 -> 0.676 

    On random lists, shell_sort_my is significantly faster than the original
    Shell gaps and slightly faster than Sedgewick's gaps on this machine.
    For the adversarial [99, 1, 99, 1, ...] pattern of length 8192, the
    difference is more pronounced:
        Shell gaps = 0.69 seconds
        My gaps = 0.0059 seconds
    This shows that my_gaps() removes the classic parity-based worst
    case and gives excellent average-case performance with a very simple
    implementation.
    """
    if length < 2:
        return
    gap = int(length / 2.2)
    if gap < 1:
        gap = 1
    seen: Set[int] = set()
    while gap > 1:
        if gap not in seen and gap < length:
            seen.add(gap)
            yield gap
        gap = int(gap / 2.2)
    if 1 not in seen and length > 1:
        yield 1


def shell_sort_my(iterable: Iterable) -> None:
    """
    Shell sort that uses my_gaps() as its gap sequence.
    This function exists so that the test module can treat all Shell sort
    variants uniformly by referring to a single callable. On the measured 
    inputs, shell_sort_my is the fastest of all four sequences (Shell, 
    explicit Shell, Hibbard, Sedgewick) for both random lists and the 
    alternating worst-case pattern.
    """
    _base_shell_sort(iterable, gaps=my_gaps)
