def stingy_max_henchmen(n):
    if n == 1 or n == 2:
        return 1

    else:
        # Calculating as per below formula:
        # If F(k) and F(k+1) are known, then
        # F(2k) = F(k) * (2 * F(k+1) - F(k))
        # F(2k+1) =  F(k+1)^2 + F(k)^2

        k = n / 2
        if n % 2 == 0:
            return stingy_max_henchmen(k) * (2 * stingy_max_henchmen(k + 1) - stingy_max_henchmen(k))
        else:
            return stingy_max_henchmen(k + 1) ** 2 + stingy_max_henchmen(k) ** 2


def generous_min_henchmen(n):
    return 2 ** n


def answer(total_lambs):
    # this blocks calculates max henchmen when being stingy
    total_lambs_stingy = total_lambs
    henchmen_max = 0
    i = 1
    lambs_hand_out = stingy_max_henchmen(i)

    # Being stingy follow fibonacci series
    # Hence, calling fibonacci function on while loop
    # until lambs in hand are sufficient for payout
    while total_lambs_stingy >= lambs_hand_out:
        total_lambs_stingy -= lambs_hand_out
        henchmen_max += 1

        i += 1
        lambs_hand_out = stingy_max_henchmen(i)

    # this blocks calculates min henchmen when being generous
    total_lambs_generous = total_lambs
    henchmen_min = 0
    i = 0
    lambs_hand_out = generous_min_henchmen(i)

    # As in generous case, the check is for maximum payout
    # at each level. These two variables are used when while
    # loop fails to see if payout can be made with 
    # minimum value
    prev_henchman = 0
    prev_to_prev_henchman = 0

    # Being generous follow 2^n series
    # Hence, calling function that calculates 2^n on while loop
    # until lambs in hand are sufficient for payout
    while total_lambs_generous >= lambs_hand_out:
        total_lambs_generous -= lambs_hand_out
        henchmen_min += 1

        prev_to_prev_henchman = prev_henchman
        prev_henchman = lambs_hand_out

        i += 1
        lambs_hand_out = generous_min_henchmen(i)

    # After all maximum payouts are done; checking if a final
    # payout can be made with minimum lambs in hand
    if total_lambs_generous >= prev_henchman + prev_to_prev_henchman:
        total_lambs_generous -= lambs_hand_out
        henchmen_min += 1

    return abs(henchmen_max - henchmen_min)

print answer(1000000000)
