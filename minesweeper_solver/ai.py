import random

from virtual_board import Board

CLICK_ACTION = 1
FLAG_ACTION = 0

# Returns - Set of (x, y, action [0 Flag, 1 Click])
def get_next_moves(board: Board, first=False) -> set:
    if first:
        return get_random_move(board)
    
    basic_moves = basic_algorithm(board)
    if (len(basic_moves) > 0):
        return basic_moves
    
    return prob_algorithm(board)

def get_random_move(board: Board) -> set:
    moves = set()
    tiles = board.get_undiscovered_tiles()
    if tiles:
        random_tile = random.choice(tiles)
        moves.add((random_tile.x, random_tile.y, CLICK_ACTION))
    return moves


# Standard Minesweeper Algortim
def basic_algorithm(board: Board) -> set:
    moves = set()
    for tile in board.get_border_tiles():
        remaining_mines = board.remaining_nearby_mines(tile)
        surrounding = board.get_surrounding_tiles(tile)
        unrevealed_surrounding = [t for t in surrounding if t.value is None]
        chance_of_mine = remaining_mines / len(unrevealed_surrounding)
        for space in unrevealed_surrounding:
            if chance_of_mine == 1:
                moves.add((space.x, space.y, FLAG_ACTION))
            elif chance_of_mine == 0:
                moves.add((space.x, space.y, CLICK_ACTION))
    return moves

# Guess the best possible move remaining
def prob_algorithm(board: Board) -> set:
    moves = set()
    width = board.horizontal_tiles
    height = board.vertical_tiles
    probabilities = [[-1 for _ in range(width)] for _ in range(height)]
    
    # Calculate Probabilities
    for tile in board.get_undiscovered_borders():
        num_adjacent_mines = 0
        num_adjacent_unknowns = 0
        for sur_tile in board.get_surrounding_tiles(tile):
            if sur_tile.value == -1:
                num_adjacent_mines += 1
            elif sur_tile.value is None and not sur_tile.value == -1:
                num_adjacent_unknowns += 1
        # Count the number of adjacent mines and unknown cells.

        if num_adjacent_unknowns != 0:
            probabilities[tile.y][tile.x] = num_adjacent_mines / num_adjacent_unknowns
        # Calculate the probability that the cell is a mine, given the adjacent cells.

    max_probability = -1
    best_move = None
    for row in range(height):
        for col in range(width):
            if probabilities[row][col] > max_probability:
                max_probability = probabilities[row][col]
                best_move = (col, row, 1)
    moves.add(best_move)
    return moves