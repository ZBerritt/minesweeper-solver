import ai.neural_network
from solver.board import Board
from solver.solver import Action, Solver


class SolverAi(Solver):
    # Returns - Set of (x, y, action)
    def get_next_moves(board: Board, no_guess=True) -> set[tuple[int, int, Action]]:
        pass
    