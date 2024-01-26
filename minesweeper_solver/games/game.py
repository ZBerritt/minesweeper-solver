from __future__ import annotations
from abc import abstractmethod, ABC
from enum import Enum
from solver.board import Board

"""
Game: Represents and arbitrary game board that is shown on the screen
- width: Number of boxes in the x direction
- height: Number of boxes in the y direction
- delay: Default number of seconds to delay the next move
"""
class Game(ABC):
    def __init__(self, name: str, width: int, height: int, delay: int):
        self.name = name
        self.width = width
        self.height = height
        self.delay = delay
        self.board = Board(self.width, self.height)

    # Abstracts
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def status(self) -> Status:
        pass

    @abstractmethod
    def create(self) -> Game:
        pass
    
    @abstractmethod
    def flag_action(self, x, y):
        pass
    
    @abstractmethod
    def click_action(self, x, y):
        pass

class Status(Enum):
    INPROGRESS = 0
    LOST = 1
    WON = 2
    STUCK = 3