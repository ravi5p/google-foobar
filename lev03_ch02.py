def answer(l):

    l_len = len(l)

    divisors_tracker = [0] * l_len
    lucky_triples = 0

    for i in xrange(l_len):
        for j in xrange(i):
            if l[i] % l[j] == 0:
                divisors_tracker[i] += 1

                # every time, i is divided by j
                # we're adding the count of divisors of j
                # as these three numbers form a triplet
                lucky_triples += divisors_tracker[j]

    return lucky_triples

print answer([1, 2, 3, 4, 5, 6])
