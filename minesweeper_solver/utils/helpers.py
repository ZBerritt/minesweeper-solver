# Is the color given near any target colors
def near_same_color(color, targets, tolerance=5):
    return any(abs(color[0] - target[0]) <= tolerance
               and abs(color[1] - target[1]) <= tolerance
               and abs(color[2] - target[2]) <= tolerance for target in targets)
    
def surrounding_tiles(x, y, width, height):
    tiles = []
    positions = [
        (x - 1, y - 1),  # Above-Left
        (x, y - 1),      # Above
        (x + 1, y - 1),  # Above-Right
        (x + 1, y),      # Right
        (x + 1, y + 1),  # Bottom-Right
        (x, y + 1),      # Bottom
        (x - 1, y + 1),  # Bottom-Left
        (x - 1, y),      # Left
    ]
    for pos in positions:
        px, py = pos
        if 0 <= px < width and 0 <= py < height:
            tiles.append((px, py))
    return tiles