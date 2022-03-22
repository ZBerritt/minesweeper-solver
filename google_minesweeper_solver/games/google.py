import pyautogui

from google_minesweeper_solver import virtual_board
from google_minesweeper_solver.util import near_same_color


# TODO - Get board that's partially complete
def get_board():
    im = pyautogui.screenshot()
    top_left = None
    bottom_right = None
    top_right = None
    box_one_top_right = None
    box_one_bottom_left = None
    for y in range(im.height):
        if bottom_right:
            break
        for x in range(im.width):
            pixel = im.getpixel((x, y))
            if not top_left and near_same_color(pixel, (170, 215, 81)):  # First green box
                top_left = (x, y)
            elif top_left and not box_one_top_right and near_same_color(pixel, (162, 209, 73)):
                box_one_top_right = (x - 1, y)
            elif box_one_top_right and not top_right and not (near_same_color(pixel, (162, 209, 73))
                                                              or near_same_color(pixel, (170, 215, 81))):  # Off screen
                top_right = (x - 1, y)
            elif top_right and not box_one_bottom_left and x == top_left[0] and near_same_color(pixel, (162, 209, 73)):
                box_one_bottom_left = (x, y - 1)
            elif box_one_bottom_left and not bottom_right \
                    and x == top_right[0] and not (near_same_color(pixel, (162, 209, 73))
                                                   or near_same_color(pixel, (170, 215, 81))):
                bottom_right = (x, y - 1)

    if not bottom_right:
        return None

    box_dimensions = (box_one_top_right[0] - top_left[0] + 1, box_one_bottom_left[1] - top_left[1] + 1)
    board_dimensions = (top_right[0] - top_left[0] + 1, bottom_right[1] - top_left[1] + 1)
    return GoogleBoard(top_left, board_dimensions, box_dimensions)


class GoogleBoard:
    def __init__(self, top_left, board_dimensions, box_dimensions):
        self.top_left = top_left
        self.dimensions = board_dimensions
        self.box_dimensions = box_dimensions

        # Get virtual board
        self.virtual_board = virtual_board.Board(self.boxes_horizontal(), self.boxes_vertical())
        self.virtual_board.populate_board(self.get_tile_values())

    def boxes_horizontal(self):
        return int(self.dimensions[0] / self.box_dimensions[0])

    def boxes_vertical(self):
        return int(self.dimensions[1] / self.box_dimensions[1])

    def box_count(self):
        return self.boxes_vertical() * self.boxes_horizontal()

    def get_mouse_position(self, x, y):  # x and y are defined over the board, not the screen (box 1 is {0, 0])
        # Get the position of the box
        tr_x_pos = self.top_left[0] + (self.box_dimensions[0] * x)
        tr_y_pos = self.top_left[1] + (self.box_dimensions[1] * y)
        x_pos = tr_x_pos + round(self.box_dimensions[0] / 2)
        y_pos = tr_y_pos + round(self.box_dimensions[1] / 2)
        return x_pos, y_pos

    def tile_range(self, x, y):
        left_x = self.top_left[0] + (self.box_dimensions[0] * x)
        top_y = self.top_left[1] + (self.box_dimensions[1] * y)
        right_x = left_x + self.box_dimensions[0] - 1
        bottom_y = top_y + self.box_dimensions[1] - 1
        return [[left_x, right_x], [top_y, bottom_y]]

    # TODO - The value recognition by color is completely busted AND slow as balls
    def tile_value(self, x, y):
        screen = pyautogui.screenshot()
        positions = self.tile_range(x, y)

        for y in range(positions[1][0], positions[1][1]):
            for x in range(positions[0][0], positions[0][1]):
                pixel = screen.getpixel((x, y))
                if near_same_color(pixel, google_colors["light_empty"]) or near_same_color(pixel,
                                                                                           google_colors["dark_empty"]):
                    return None
                elif near_same_color(pixel, google_colors["one"], 10):
                    return 1
                elif near_same_color(pixel, google_colors["three"], 10):
                    return 2
                elif near_same_color(pixel, google_colors["two"], 10):
                    return 3
        return 0

    # Pretty slow, maybe need to start combining stuff
    def get_tile_values(self):
        values = []
        row_num = -1
        for y in range(0, self.boxes_horizontal() - 1):
            row_num += 1
            values.append([])
            for x in range(0, self.boxes_vertical() - 1):
                values[row_num].append(self.tile_value(x, y))
        return values


google_colors = {
    "light_empty": (170, 215, 81),
    "dark_empty": (162, 209, 73),
    "light_open": (224, 195, 163,),
    "dark_open": (211, 185, 157),
    "border": (126, 164, 53),
    "flag": (242, 54, 7),
    # The colors are gradients, but as long as the color shows on the square its a number
    "one": (25, 118, 210),
    "two": (55, 141, 59),
    "three": (211, 47, 47)
}