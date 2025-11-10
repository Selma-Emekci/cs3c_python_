# is_prime() and next_prime() can be found in modules like sympy.
# They are defined here to avoid having to install additional modules.

def is_prime(n):
    """
    Check if n is a prime number
    :param n: number to check for primality
    :return: True if n is prime, False otherwise
    """
    # https://en.wikipedia.org/wiki/Primality_test
    # Corner cases
    if n <= 1:
        return False
    if n <= 3:
        return True

    # This is checked so that we can skip
    # middle five numbers in below loop
    if n % 2 == 0 or n % 3 == 0:
        return False

    # So we start at 6k±1, k=1, so that's 5, and 7.
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i = i + 6

    return True


def next_prime(floor):
    """
    Return the next prime number that's larger than floor
    :param floor:
    :return:
    """
    if floor < 2:
        return 2
    if floor < 3:
        return 3

    # The next prime should start at the next odd number bigger than floor
    candidate = floor + 1
    if candidate % 2 == 0:
        candidate += 1

    while True:
        if is_prime(candidate):
            return candidate
        candidate += 2
