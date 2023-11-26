import random
from enum import Enum
from board.virtual_board import Board


class Action(Enum):
    CLICK = 1
    FLAG = 0

# Returns - Set of (x, y, action)
def get_next_moves(board: Board) -> set:
    if all(tile.value == None for tile in board.get_all_tiles()):
        return get_random_move(board)
    
    basic_moves = basic_algorithm(board)
    if len(basic_moves) > 0:
        return basic_moves
    
    return prob_algorithm(board)

def get_random_move(board: Board) -> set:
    moves = set()
    tiles = board.get_undiscovered_tiles()
    if tiles:
        random_tile = random.choice(tiles)
        moves.add((random_tile.x, random_tile.y, Action.CLICK))
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
                moves.add((space.x, space.y, Action.FLAG))
            elif chance_of_mine == 0:
                moves.add((space.x, space.y, Action.CLICK))
    return moves

def prob_algorithm(board: Board) -> set:
    borders = board.get_undiscovered_borders()
    probabilities = [-1 for _ in borders]
    for i, tile in enumerate(borders):
        num_adjacent_mines = 0
        num_adjacent_unknowns = 0
        for sur_tile in board.get_surrounding_tiles(tile):
            if sur_tile.value == -1:
                num_adjacent_mines += 1
            elif sur_tile.value is None:
                num_adjacent_unknowns += 1

        if num_adjacent_unknowns != 0:
            probabilities[i] = num_adjacent_mines / num_adjacent_unknowns
    
    best_tile = max(zip(borders, probabilities), key=lambda x: x[1], default=(None, -1))[0]
    return set([(best_tile.x, best_tile.y, Action.CLICK)]) if best_tile else set()
    