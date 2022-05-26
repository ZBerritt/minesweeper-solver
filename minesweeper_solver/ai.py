# Not a real AI but it sounds cooler
import random


# Returns - [(x, y, action (0 Flag, 1 Click), ...] OR None if no moves were found.
def get_next_moves(board, first=False):
    # Return a random space if it's the first move
    if first:
        tiles = board.get_empty_tiles()
        if len(tiles) == 0:
            return None
        random_tile = tiles[random.randrange(0, len(tiles))]
        return {(random_tile[0], random_tile[1], 1)}

    # Variables
    border_tiles = board.get_border_tiles()
    undiscovered_borders = board.get_undiscovered_borders()

    # Moves to return
    moves = set()

    # Basic Algorithm
    for tile in border_tiles:
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

    # TODO: Standard Algorithm

    # TODO: Probability Algorithm

    return None
