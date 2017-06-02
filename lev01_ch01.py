import math


def answer(n):
    # your code here
    prime_number_string = prime_generator()

    return prime_number_string[n:n + 5]


def prime_generator():
    is_prime_arr = [False, False]

    # since the n value boundary is defined, so hard-coded
    # number that caters to all cases in [0 10000]
    primes_under_num = 21000
    for i in range(2, primes_under_num):
        is_prime_arr.append(True)

    for i in range(2, int(math.sqrt(primes_under_num))):
        if is_prime_arr[i] is True:
            j = i ** 2
            while j < primes_under_num:
                is_prime_arr[j] = False
                j += i

    string_of_all_primes = ''

    for i in range(primes_under_num):
        if is_prime_arr[i] is True:
            string_of_all_primes += str(i)

    # print len(string_of_all_primes)
    return string_of_all_primes

print answer(10000)
