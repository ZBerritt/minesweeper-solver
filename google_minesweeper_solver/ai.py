# Not a real AI but it sounds cooler
import random


# Gets the next move that the solver should use
# Returns - Move object if move is found, None otherwise
def get_next_move(board):
    border_tiles = board.get_border_tiles()

    for tile in border_tiles:
        # Super Mega Basic Algorithm
        remaining_mines = board.remaining_nearby_mines(tile[0], tile[1])
        surrounding = board.get_surrounding_tiles(tile[0], tile[1])
        unrevealed_surrounding = [t for t in surrounding if t[2].value is None]
        chance_of_mine = remaining_mines / len(unrevealed_surrounding)
        if chance_of_mine == 1:
            return Move(unrevealed_surrounding[0][0], unrevealed_surrounding[0][1], 0)
        elif chance_of_mine == 0:
            return Move(tile[0], tile[1], 0)

    # All else fails, random shot in the dark
    return Move(random.randrange(0, board.horizontal_tiles - 1), random.randrange(0, board.vertical_tiles), 1)


class Move:
    def __init__(self, x, y, action):
        self.x = x
        self.y = y
        self.action = action  # 0 - Flag, 1 - Click
