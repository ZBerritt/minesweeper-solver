from __future__ import annotations
from abc import abstractmethod, ABC
from PIL import Image
from board.board import Board
from utils.screenshot import screenshot

"""
Game: Represents and arbitrary game board that is shown on the screen
- position: The position of the top left of the board
- dimensions: The full dimensions of the board (length, height)
- box_dimensions: The full dimensions of a singular box (length, height)
- delay: Default number of seconds to delay the next move
"""
class Game(ABC):
    def __init__(self, name, position, dimensions, box_dimensions, delay):
        self.name = name
        self.position = position
        self.dimensions = dimensions
        self.box_dimensions = box_dimensions
        self.boxes_horizontal = int(self.dimensions[0] / self.box_dimensions[0])
        self.boxes_vertical = int(self.dimensions[1] / self.box_dimensions[1])
        self.delay = delay
        self.board = Board(self.boxes_horizontal, self.boxes_vertical)

    # Global Game Functions
    def box_count(self) -> int:
        return self.boxes_vertical * self.boxes_horizontal

    def get_mouse_position(self, board_x_pos: int, board_y_pos: int) -> tuple[int, int]:
        top_right_x_pos = self.position[0] + (self.box_dimensions[0] * board_x_pos)
        top_right_y_pos = self.position[1] + (self.box_dimensions[1] * board_y_pos)
        mouse_x_pos = top_right_x_pos + round(self.box_dimensions[0] / 2)
        mouse_y_pos = top_right_y_pos + round(self.box_dimensions[1] / 2)
        return mouse_x_pos, mouse_y_pos

    def tile_range(self, board_x_pos: int, board_y_pos: int) -> tuple[tuple[int, int], tuple[int, int]]:
        left_x = self.position[0] + (self.box_dimensions[0] * board_x_pos)
        top_y = self.position[1] + (self.box_dimensions[1] * board_y_pos)
        right_x = left_x + self.box_dimensions[0] - 1
        bottom_y = top_y + self.box_dimensions[1] - 1
        return (left_x, right_x), (top_y, bottom_y)

    def update(self):
        screen = screenshot()
        tiles = self.board.get_undiscovered_tiles()
        for tile in tiles:
            self.board.set_value(tile.x, tile.y, self.tile_value(tile.x, tile.y, screen))
            
    # Abstracts
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
