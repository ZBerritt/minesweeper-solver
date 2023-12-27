# Is the color given near any target colors
from typing import Callable


def near_same_color(color: tuple[int, int, int], targets: tuple[int, int, int], tolerance=5):
    return any(abs(color[0] - target[0]) <= tolerance
               and abs(color[1] - target[1]) <= tolerance
               and abs(color[2] - target[2]) <= tolerance for target in targets)
    
def surrounding_tiles(x: int, y: int, width: int, height: int, callback: Callable[[int, int], any]) -> list[any]:
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
    return [callback(px, py) for px, py in positions if 0 <= px < width and 0 <= py < height]