import random
from enum import Enum
import numpy as np
from solver.board import Board, FLAGGED
from solver.solver import Action, Solver

class SolverBasic(Solver):
    def get_next_moves(board: Board, no_guess=True) -> set[tuple[int, int, Action]]:
        if all(tile.value == None for tile in board.get_all_tiles()):
            return get_random_move(board)
        
        moves = basic_recursive_moves(board, set())
        if not moves and not no_guess:
            moves = prob_algorithm(board)
        return moves

def basic_recursive_moves(board: Board, result_moves: set[tuple[int, int, Enum]]) -> set[tuple[int, int, Enum]]:
    basic_moves = basic_algorithm(board)
    combined_moves = basic_moves.union(result_moves)
    if combined_moves == result_moves:
        return result_moves

    for move in basic_moves:
        x, y, action = move
        if action == Action.FLAG:
            board.set_value(x, y, FLAGGED)

    return basic_recursive_moves(board, combined_moves)

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
    best_tile = None
    best_prob = -1
    tiles = board.get_undiscovered_borders()
    for tile in tiles:
        probs = []
        for sur_tile in board.get_surrounding_tiles(tile):
            surrounding_mines = board.remaining_nearby_mines(sur_tile)
            if surrounding_mines > 0:
                probs.append(1 / surrounding_mines)
        avg_prob = np.average(probs)
        if avg_prob > best_prob:    
            best_tile = tile
            best_prob = avg_prob

    return set([(best_tile.x, best_tile.y, Action.CLICK)]) if best_tile else get_random_move(board)
    