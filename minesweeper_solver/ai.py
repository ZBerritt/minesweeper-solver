# Not a real AI but it sounds cooler
import random


# Gets the next move that the solver should use
# Returns - (x, y, action (0 Flag, 1 Click). None indicates the game is lost
def get_next_moves(board, first=False):
    if first:
        tiles = board.get_empty_tiles()
        if len(tiles) == 0:
            return None
        random_tile = tiles[random.randrange(0, len(tiles))]
        return {(random_tile[0], random_tile[1], 1)}  # Random move on first move
    border_tiles = board.get_border_tiles()

    moves = set()
    for tile in border_tiles:
        # Super Mega Basic Algorithm
        remaining_mines = board.remaining_nearby_mines(tile[0], tile[1])
        surrounding = board.get_surrounding_tiles(tile[0], tile[1])
        unrevealed_surrounding = [t for t in surrounding if t[2].value is None]
        chance_of_mine = remaining_mines / len(unrevealed_surrounding)
        for space in unrevealed_surrounding:
            if chance_of_mine == 1:
                moves.update([(space[0], space[1], 0)])
            elif chance_of_mine == 0:
                moves.update([(space[0], space[1], 1)])
    if len(moves) > 0:
        return moves

    return None
