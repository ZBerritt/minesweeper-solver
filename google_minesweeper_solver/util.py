def near_same_color(color, target, tolerance=5):
    return abs(color[0] - target[0]) <= tolerance \
        and abs(color[1] - target[1]) <= tolerance \
        and abs(color[2] - target[2]) <= tolerance
