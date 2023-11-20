from abc import abstractmethod, ABC
import pyautogui
import virtual_board

# Fix for duel monitors
from PIL import ImageGrab
from functools import partial

ImageGrab.grab = partial(ImageGrab.grab, all_screens=True)


def get_screen():
    return pyautogui.screenshot()


# Represents and arbitrary game board that is shown on the screen
class Game(ABC):
    def __init__(self, name, top_left, board_dimensions, box_dimensions, move_delay):
        self.name = name
        self.top_left = top_left
        self.dimensions = board_dimensions
        self.box_dimensions = box_dimensions
        self.move_delay = move_delay
        self.boxes_horizontal = int(self.dimensions[0] / self.box_dimensions[0])
        self.boxes_vertical = int(self.dimensions[1] / self.box_dimensions[1])

        # Get virtual board
        self.virtual_board = virtual_board.Board(self.boxes_horizontal, self.boxes_vertical)
        self.update()

    # Global Game Functions
    def box_count(self) -> int:
        return self.boxes_vertical * self.boxes_horizontal

    def get_mouse_position(self, x, y) -> tuple[int, int]:  # x and y are defined over the board, not the screen (box 1 is {0, 0])
        # Get the position of the box
        tr_x_pos = self.top_left[0] + (self.box_dimensions[0] * x)
        tr_y_pos = self.top_left[1] + (self.box_dimensions[1] * y)
        x_pos = tr_x_pos + round(self.box_dimensions[0] / 2)
        y_pos = tr_y_pos + round(self.box_dimensions[1] / 2)
        return x_pos, y_pos

    def tile_range(self, x, y) -> tuple[tuple[int, int], tuple[int, int]]:
        left_x = self.top_left[0] + (self.box_dimensions[0] * x)
        top_y = self.top_left[1] + (self.box_dimensions[1] * y)
        right_x = left_x + self.box_dimensions[0] - 1
        bottom_y = top_y + self.box_dimensions[1] - 1
        return ((left_x, right_x), (top_y, bottom_y))

    def update(self):
        screen = get_screen()
        tiles = self.virtual_board.get_undiscovered_tiles()
        for tile in tiles:
            self.virtual_board.set_value(tile.x, tile.y, self.tile_value(tile.x, tile.y, screen))

    # Abstracts
    @abstractmethod
    def tile_value(self, x, y, screen):
        pass

    @abstractmethod
    def game_over(self):
        pass

