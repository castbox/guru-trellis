from bounds_policy import ordered_bounds


def contains(value, lower, upper):
    lower, upper = ordered_bounds(lower, upper)
    return lower <= value <= upper
