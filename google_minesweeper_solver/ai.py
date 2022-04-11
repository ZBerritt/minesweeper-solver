# Not a real AI but it sounds cooler
import random


# Gets the next move that the solver should use
# Returns - (x, y, action (0 Flag, 1 Click). None indicates the game is lost
def get_next_move(board):
    border_tiles = board.get_border_tiles()
    
    moves = []
    spaces = []
    for tile in border_tiles:
        # Super Mega Basic Algorithm
        remaining_mines = board.remaining_nearby_mines(tile[0], tile[1])
        surrounding = board.get_surrounding_tiles(tile[0], tile[1])
        unrevealed_surrounding = [t for t in surrounding if t[2].value is None]
        chance_of_mine = remaining_mines / len(unrevealed_surrounding)
        first_space = unrevealed_surrounding[0]
        if chance_of_mine == 1:
            return first_space[0], first_space[1], 0
        elif chance_of_mine == 0:
            return first_space[0], first_space[1], 1

    # All else fails, random shot in the dark
    tiles = board.get_empty_tiles()
    if len(tiles) == 0:
        return None
    random_tile = tiles[random.randrange(0, len(tiles))]
    return random_tile[0], random_tile[1], 1
