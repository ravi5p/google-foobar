

def pair_up(g1, g2):

    if g1 > g2:
        g1, g2 = g2, g1

    new_g1, new_g2 = g1, g2

    # running the pair verification logic for 2 times
    # as it will result in equal bananas if they can't be paired
    for i in xrange(2):

        # one iteration is defined as winning bananas until
        # one with lesser bananas end up having higher
        j = 0
        while new_g1 < new_g2:
            new_g1 += (2 ** j) * g1
            new_g2 -= (2 ** j) * g1

            j += 1

        # swapping bananas to run through login one more time
        new_g1, new_g2 = new_g2, new_g1
        g1, g2 = new_g1, new_g2

    # after two iterations, if they end up with same number of bananas,
    # then they can't be a valid pair. Else, they are.
    if g1 == g2:
        return False
    else:
        return True


def answer(banana_list):
    # total_guards = len(banana_list)

    len_banana_list = len(banana_list)

    # We're running the login until all the guards are paired up,
    # and no one left; or until we get to know no more pairs can be made
    while len_banana_list > 0:
        no_pair_found = True

        for i in xrange(len_banana_list - 1):
            pair_found = False
            for j in xrange(i + 1, len_banana_list):

                # for every combination, calling the function to
                # verify if they both can be paired up
                if pair_up(banana_list[i], banana_list[j]):
                    # print banana_list[i], banana_list[j]
                    del banana_list[i]
                    del banana_list[j - 1]
                    pair_found = True
                    no_pair_found = False
                    break
            # get out of second loop if pair is found
            if pair_found:
                break

        # after running through all combinations, if no pair
        # can be made; then its the end so coming out of the
        # program logic
        if no_pair_found:
            break

        len_banana_list = len(banana_list)

    # returning the answer as the count of guards left after doing
    # all the possible pairs
    return len(banana_list)

print answer([1, 7, 3, 21, 13, 19])
