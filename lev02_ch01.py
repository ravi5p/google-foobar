import timeit

start = timeit.default_timer()


def answer(x, y):
    # your code here

    # horizontal numbers follow series of SumOfFirstNNumbers
    # Hence, calculating with below formula:
    # sum_of_n_numbers = (n * (n + 1)) / 2

    horizontal_value = (x * (x + 1)) / 2

    # After we reach the horizontal number, we need to climb up
    # that's following similar series; but starting with x
    # Hence,
    # required value = sum_of_first_numbers_(x + y - 2) - sum_of_first_numbers(x - 1)
    #
    vertical_value = horizontal_value + ((x + y - 2) * (x + y - 1)) / 2 \
                     - ((x - 1) * x) / 2

    return str(vertical_value)

print answer(1, 100000)


print timeit.default_timer() - start
