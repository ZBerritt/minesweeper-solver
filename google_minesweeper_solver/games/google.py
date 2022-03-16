import pyautogui

from google_minesweeper_solver.virtual_board import Tile


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
            if not top_left and pixel == (170, 215, 81):  # First green box
                top_left = (x, y)
            elif top_left and not box_one_top_right and pixel == (162, 209, 73):
                box_one_top_right = (x - 1, y)
            elif box_one_top_right and not top_right and not (pixel == (162, 209, 73)
                                                              or pixel == (170, 215, 81)):  # Off screen
                top_right = (x - 1, y)
            elif top_right and not box_one_bottom_left and x == top_left[0] and pixel == (162, 209, 73):
                box_one_bottom_left = (x, y - 1)
            elif box_one_bottom_left and not bottom_right \
                    and x == top_right[0] and not (pixel == (162, 209, 73)
                                                   or pixel == (170, 215, 81)):
                bottom_right = (x, y - 1)

    if not top_left:
        return None

    box_dimensions = (box_one_top_right[0] - top_left[0] + 1, box_one_bottom_left[1] - top_left[1] + 1)
    board_dimensions = (top_right[0] - top_left[0] + 1, bottom_right[1] - top_left[1] + 1)
    return GoogleBoard(top_left, board_dimensions, box_dimensions)


class GoogleBoard:
    def __init__(self, top_left, board_dimensions, box_dimensions):
        self.top_left = top_left
        self.dimensions = board_dimensions
        self.box_dimensions = box_dimensions

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
