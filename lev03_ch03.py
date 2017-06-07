# reference:
# http://www.geeksforgeeks.org/calculate-xor-1-n/


import timeit

start1 = timeit.default_timer()


def calc_xor(a):

    a_mod_4 = a % 4

    if a_mod_4 == 0:
        return a
    elif a_mod_4 == 1:
        return 1
    elif a_mod_4 == 2:
        return a + 1
    elif a_mod_4 == 3:
        return 0


def answer(start, length):

    # bits_dictionary = [0] * 31

    first_num = start
    last_num = start + length - 1

    sub_solution = []

    loop = 0
    while length >= 1:

        # print "first_num, last_num", first_num, last_num

        # calculating xor of n1 to n2 (n1 <= n2) as below:
        # xor(n1 to n2) = xor(1 to n2) ^ xor(1 to n1)
        if first_num == 0 or first_num == 1:
            sub_solution.append(calc_xor(last_num))
        else:
            sub_solution.append(calc_xor(last_num) ^ calc_xor(first_num - 1))

        length -= 1

        first_num = last_num + 1 + loop
        last_num = first_num + length - 1

        loop += 1

    ans = 0
    for num in sub_solution:
        ans ^= num

    # return ans, sub_solution
    return ans


print answer(17, 4)

print timeit.default_timer() - start1

