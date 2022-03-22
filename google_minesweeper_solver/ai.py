# Not a real AI but it sounds cooler


# Gets the next move that the solver should use
# Returns - Move object if move is found, None otherwise
def get_next_move(board):
    for y in range(0, board.vertical_tiles - 1):
        for x in range(0, board.horizontal_tiles - 1):
            tile = board.get_space(x, y)
            if tile.solved:  # Speeds things up
                pass
            # Super mega ultra basic algorithm
            # Will do this later
    return Move(0, 0, 0)


class Move:
    def __init__(self, x, y, action):
        self.x = x
        self.y = y
        """
        Action:
        0 - Flag
        1 - Click
        """
        self.action = action
