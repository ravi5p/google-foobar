from fractions import gcd
import timeit

start = timeit.default_timer()


def get_reflection(original, direction, direction_values):
    # returns the reflection of given point
    if direction == 'R' or direction == 'L':
        return 2 * direction_values[direction] - original[0], original[1]
    else:
        return original[0], 2 * direction_values[direction] - original[1]


def add_invalid_slopes(commander, guard, room, slopes_verified_set):
    # addling slopes from commander to guard and room corners to this
    # set variable so these are not included in counting the final answer
    corner01 = 0, 0
    corner02 = room[0], 0
    corner03 = room[0], room[1]
    corner04 = 0, room[1]
    temp = [corner01, corner02, corner03, corner04, guard]
    for x, y in temp:
        x_diff = commander[0] - x
        y_diff = commander[1] - y
        x_diff_y_diff_gcd = abs(gcd(x_diff, y_diff))
        if x_diff_y_diff_gcd != 0:
            x_diff /= x_diff_y_diff_gcd
            y_diff /= x_diff_y_diff_gcd

        slopes_verified_set.add((x_diff, y_diff))

    return slopes_verified_set


def get_all_reflections(original, position, positions_verified_dict, direction, direction_values,
                        distance_square, reflections_dict, reflections_set, reflections_arr, who):
    # This function returns all valid reflection points of given point.
    # It is called two times -- once for commander and once for guard.

    # Its based on DFS; below is the exit condition.
    if (position[0] < 0 or position[0] > direction_values['R']) and \
            (position[1] < 0 or position[1] > direction_values['T']):
        try:
            if positions_verified_dict[position] > 1:
                return reflections_dict, reflections_set, reflections_arr, positions_verified_dict
            else:
                positions_verified_dict[position] += 1
        except KeyError:
            positions_verified_dict[position] = 1

    position = get_reflection(position, direction, direction_values)

    x_diff = original[0] - position[0]
    y_diff = original[1] - position[1]

    d_square = x_diff ** 2 + y_diff ** 2

    if d_square <= distance_square:
        # when the function is called for commander, updating the corresponding variables
        if who == 'C':
            x_diff_y_diff_gcd = abs(gcd(x_diff, y_diff))
            if x_diff_y_diff_gcd != 0:
                x_diff /= x_diff_y_diff_gcd
                y_diff /= x_diff_y_diff_gcd

            reflections_set.add((x_diff, y_diff))

            try:
                d_temp = reflections_dict[(x_diff, y_diff)]
                if d_square < d_temp:
                    reflections_dict[(x_diff, y_diff)] = d_square
            except KeyError:
                reflections_dict[(x_diff, y_diff)] = d_square
        # when the function is called for guard, updating the corresponding variables
        else:
            reflections_arr.add(position)

        for _direction in direction_values:
            # once light is reflected from a direction, then it is reflected on all other
            # three directions to calculate possible reflection points
            if _direction != direction:
                if _direction == 'R' and position[0] < direction_values['R']:
                    reflections_dict, reflections_set, reflections_arr, positions_verified_dict = get_all_reflections(
                        original, position,
                        positions_verified_dict,
                        _direction,
                        direction_values,
                        distance_square,
                        reflections_dict,
                        reflections_set, reflections_arr, who)

                elif _direction == 'L' and position[0] > 0:
                    reflections_dict, reflections_set, reflections_arr, positions_verified_dict = get_all_reflections(
                        original, position,
                        positions_verified_dict,
                        _direction,
                        direction_values,
                        distance_square,
                        reflections_dict,
                        reflections_set, reflections_arr, who)

                elif _direction == 'T' and position[1] < direction_values['T']:
                    reflections_dict, reflections_set, reflections_arr, positions_verified_dict = get_all_reflections(
                        original, position,
                        positions_verified_dict,
                        _direction,
                        direction_values,
                        distance_square,
                        reflections_dict,
                        reflections_set, reflections_arr, who)

                elif _direction == 'B' and position[1] > 0:
                    reflections_dict, reflections_set, reflections_arr, positions_verified_dict = get_all_reflections(
                        original, position,
                        positions_verified_dict,
                        _direction,
                        direction_values,
                        distance_square,
                        reflections_dict,
                        reflections_set, reflections_arr, who)

    return reflections_dict, reflections_set, reflections_arr, positions_verified_dict


def calc_answer((cx, cy), target_reflections_arr, distance_square, source_reflections_slope_set,
                source_reflections_slope_dist_dict, shoot_slopes_verified):
    # This function calculates the final answer to challenge.
    ans_temp = 0
    for gx, gy in target_reflections_arr:
        x_diff = cx - gx
        y_diff = cy - gy

        d_square = x_diff ** 2 + y_diff ** 2

        if d_square <= distance_square:
            x_diff_y_diff_gcd = abs(gcd(x_diff, y_diff))
            if x_diff_y_diff_gcd != 0:
                x_diff /= x_diff_y_diff_gcd
                y_diff /= x_diff_y_diff_gcd

            if (x_diff, y_diff) not in shoot_slopes_verified:
                if (x_diff, y_diff) in source_reflections_slope_set:
                    if d_square < source_reflections_slope_dist_dict[(x_diff, y_diff)]:
                        ans_temp += 1
                        shoot_slopes_verified.add((x_diff, y_diff))

                else:
                    ans_temp += 1
                    shoot_slopes_verified.add((x_diff, y_diff))

    return ans_temp


def answer(dimensions, your_position, guard_position, distance):
    # defining all the variables
    distance_square = distance ** 2
    cx, cy = your_position[0], your_position[1]
    gx, gy = guard_position[0], guard_position[1]
    rx, ry = dimensions[0], dimensions[1]

    # initializing count with 1 if the distance is >= direct hit distance. Else, return 0.
    if (cx - gx) ** 2 + (cy - gy) ** 2 <= distance_square:
        ans = 1
    else:
        return 0

    shoot_slopes_verified = set([])
    shoot_slopes_verified_set = add_invalid_slopes((cx, cy), (gx, gy), (rx, ry), shoot_slopes_verified)

    # For commander, only a set variable that holds slopes of commander reflections; and a dictionary variable that
    # holds distances of these reflection points from commander are needed.
    # And for guard, only a set variable that holds all the reflection points is needed.
    # But to re-use same function to calculate all reflection points for both commander and guard, additional variables
    # are declared that are never used.
    source_reflections_arr = set([])
    source_reflections_slope_set = set([])
    source_reflections_slope_dist_dict = {}

    target_reflections_arr = set([])
    target_reflections_slope_set = set([])
    target_reflections_slope_dist_dict = {}

    # Below dictionary is to help calculate reflections w.r.t top, bottom
    # left and right sides of rectangle
    direction_values = {'R': dimensions[0], 'L': 0, 'T': dimensions[1], 'B': 0}
    directions = ['R', 'L', 'T', 'B']

    # First, get_all_reflections function is called to identify all the reflections of commander,
    # slope of all these reflection points is added to set, and distance of these reflection points
    # are added to dictionary with slope as key. This is used to verify if a direction at guard
    # overlaps with commander and if yes, will it first hit commander.
    positions_verified_dict = {}
    for direction in directions:
        source_reflections_slope_dist_dict, source_reflections_slope_set, \
        source_reflections_arr, positions_verified_dict = \
            get_all_reflections((cx, cy), (cx, cy),
                                positions_verified_dict, direction, direction_values, distance_square,
                                source_reflections_slope_dist_dict,
                                source_reflections_slope_set, source_reflections_arr, 'C')

    # Secondly, same get_all_reflections function is called to identify all the reflection points of guard,
    # and are added to a set variable.
    positions_verified_dict = {}
    for direction in directions:
        target_reflections_slope_dist_dict, target_reflections_slope_set, \
        target_reflections_arr, positions_verified_dict = \
            get_all_reflections((cx, cy), (gx, gy),
                                positions_verified_dict, direction, direction_values, distance_square,
                                source_reflections_slope_dist_dict,
                                source_reflections_slope_set, source_reflections_arr, 'G')

    # After initializing count with 1 for direct hit, calc_answer function is called that takes each guard reflection,
    # calculates slope at guard reflection, checks if it overlaps with commander. If yes, checks if commander
    # is hit first or guard. If it hits guard first, count is incremented; else, not. If it doesn't overlap with
    # slope of commander, count is incremented. And the slope is marked as verified so it won't be re-calculated.
    ans += calc_answer((cx, cy), target_reflections_arr, distance_square, source_reflections_slope_set,
                       source_reflections_slope_dist_dict, shoot_slopes_verified_set)

    return ans


# print answer([3, 2], [1, 1], [2, 1], 20)
# print answer([300, 275], [150, 150], [185, 100], 500)
# print answer([2, 5], [1, 2], [1, 4], 11)
print answer([42, 59], [34, 44], [6, 34], 5000)

print timeit.default_timer() - start
