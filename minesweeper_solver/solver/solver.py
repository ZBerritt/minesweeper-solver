from abc import ABC
import random
from enum import Enum
import numpy as np
from solver.board import Board, FLAGGED


class Action(Enum):
    CLICK = 1
    FLAG = 0

class Solver(ABC):
    # Returns - Set of (x, y, action)
    def get_next_moves(board: Board, no_guess=True) -> set[tuple[int, int, Action]]:
        pass