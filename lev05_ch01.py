# reference:
# https://oeis.org/A001951
# https://en.wikipedia.org/wiki/Beatty_sequence

from decimal import *
import timeit

getcontext().prec = 150

start = timeit.default_timer()


def beatty_sequence(num, sqrt_of_2):
    # Per beatty sequence,
    # S(x, n) = (n + n') * (n + n' + 1) / 2 - S(y, n'); where
    # n' = floor((x - 1) * n)
    # (1/x) + (1/y) = 1
    # Here, x = sqrt(2) ==> y = 2 + sqrt(2)
    # S(sqrt(2), n) = n n' + n (n + 1) / 2 - n' (n' + 1) / 2 - S(y, n')
    if num == 0:
        return 0
    else:
        num_reduced = int(num * (sqrt_of_2 - 1))
        prod_01 = num * num_reduced
        prod_02 = num * (num + 1) / 2
        prod_03 = num_reduced * (num_reduced + 1) / 2

        return prod_01 + prod_02 - prod_03 - beatty_sequence(num_reduced, sqrt_of_2)


def answer(str_n):

    sqrt_of_2 = Decimal(2).sqrt()
    return beatty_sequence(int(str_n), sqrt_of_2)

print answer(10 ** 100)

print timeit.default_timer() - start
