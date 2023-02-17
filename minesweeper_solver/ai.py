# Not a real AI but it sounds cooler
import random


# Returns - {(x, y, action (0 Flag, 1 Click), ...} OR None if no moves were found.
def get_next_moves(board, first=False):
    # Return a random space if it's the first move
    if first:
        tiles = board.get_empty_tiles()
        if not tiles:
            return None
        random_tile = random.choice(tiles)
        return {(random_tile[0], random_tile[1], 1)}

    # Moves to return
    moves = set()

    # Basic Algorithm
    # Super quick but doesn't always find a solution
    for tile in board.get_border_tiles():
        remaining_mines = board.remaining_nearby_mines(tile[0], tile[1])
        surrounding = board.get_surrounding_tiles(tile[0], tile[1])
        unrevealed_surrounding = [t for t in surrounding if t[2].value is None]
        chance_of_mine = remaining_mines / len(unrevealed_surrounding)
        for space in unrevealed_surrounding:
            if chance_of_mine == 1:
                moves.update([(space[0], space[1], 0)])
            elif chance_of_mine == 0:
                moves.update([(space[0], space[1], 1)])
    if moves:
        return moves

    # TODO: Standard Algorithm
    # Uses some extra tricks to find any guaranteed mines or safe spaces

    # Probability Algorithm - Guessing is the best tactic :)
    width = board.horizontal_tiles
    height = board.vertical_tiles
    probabilities = [[-1 for _ in range(width)] for _ in range(height)]
    for tile in board.get_undiscovered_borders():
        num_adjacent_mines = 0
        num_adjacent_unknowns = 0
        for sur_tile in board.get_surrounding_tiles(tile[0], tile[1]):
            if sur_tile[2].value == -1:
                num_adjacent_mines += 1
            elif sur_tile[2].value is None:
                num_adjacent_unknowns += 1
        # Count the number of adjacent mines and unknown cells.

        if num_adjacent_unknowns != 0:
            probabilities[tile[1]][tile[0]] = num_adjacent_mines / num_adjacent_unknowns
        # Calculate the probability that the cell is a mine, given the adjacent cells.

    max_probability = -1
    best_move = None
    for row in range(height):
        for col in range(width):
            if probabilities[row][col] > max_probability:
                max_probability = probabilities[row][col]
                best_move = (col, row, 1)
    print("I think ({0}, {1}) is safe...".format(best_move[0], best_move[1]))
    moves.add(best_move)
    return moves
