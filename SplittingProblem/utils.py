from math import ceil as math_ceil

def get_lower_bound(workpiece_lengths, max_rod_length) -> int:
    return math_ceil(sum(workpiece_lengths) / max_rod_length)

def get_deviation(best_crit, lower_bound):
    return best_crit / lower_bound - 1
