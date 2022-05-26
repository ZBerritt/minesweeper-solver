# Is the color given near any target colors
def near_same_color(color, targets, tolerance=5):
    for target in targets:
        if(abs(color[0] - target[0]) <= tolerance
                and abs(color[1] - target[1]) <= tolerance
                and abs(color[2] - target[2]) <= tolerance):
            return True
    return False
