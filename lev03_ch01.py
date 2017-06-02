def minimum_hops(num, hops_dict):

    hops = 0
    while num != 1:
        if num % 2 == 0:
            num /= 2
            hops += 1
        else:

            try:
                num_minus_one_hops = hops_dict[num - 1]
            except KeyError:
                num_minus_one_hops = minimum_hops(num - 1, hops_dict)
                hops_dict[num - 1] = num_minus_one_hops

            # print "after first call: prev hops, num - 1 hops", hops, num_minus_one_hops

            try:
                num_plus_one_hops = hops_dict[num + 1]
            except KeyError:
                num_plus_one_hops = minimum_hops(num + 1, hops_dict)
                hops_dict[num + 1] = num_plus_one_hops

            # print "after second call: prev hops, num + 1 hops", hops, num_plus_one_hops

            hops += 1 + min(num_minus_one_hops, num_plus_one_hops)
            hops_dict[num] = hops
            num = 1

    return hops


def answer(n):
    hops_dictionary = {}

    return minimum_hops(int(n), hops_dictionary)

# print answer(10 ** 309)
