from __future__ import annotations
from abc import abstractmethod, ABC
from PIL import Image
from board.board import Board
from utils.screenshot import screenshot

"""
Game: Represents and arbitrary game board that is shown on the screen
- boxes_horizontal: Number of boxes in the x direction
- boxes_vertical: Number of boxes in the y direction
- delay: Default number of seconds to delay the next move
"""
class Game(ABC):
    def __init__(self, name: str, boxes_horizontal: int, boxes_vertical: int, delay: int):
        self.name = name
        self.boxes_horizontal = boxes_horizontal
        self.boxes_vertical = boxes_vertical
        self.delay = delay
        self.board = Board(self.boxes_horizontal, self.boxes_vertical)

    # Abstracts
    @abstractmethod
    def update(self):
        pass
            
    @abstractmethod
    def tile_value(self, x: int, y: int, screen: Image) -> int:
        pass
    
    # Returns 1 if a loss is detected, returns 2 if a win is detected, returns 0 otherwise
    @abstractmethod
    def status(self) -> int:
        pass

    @abstractmethod
    def get_board(self) -> Game:
        pass
    
    @abstractmethod
    def flag_action(self, x, y):
        pass
    
    @abstractmethod
    def click_action(self, x, y):
        pass
