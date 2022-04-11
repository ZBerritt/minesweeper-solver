import pyautogui

from google_minesweeper_solver import virtual_board
from google_minesweeper_solver.util import near_same_color


# TODO - Get board that's partially complete
def get_board():
    im = pyautogui.screenshot()
    top_left = None
    box_one_bottom_right = None
    bottom_right = None
    for y in range(im.height):
        if bottom_right:
            break

        if not top_left:
            for x in range(im.width):
                pixel = im.getpixel((x, y))
                if not top_left and near_same_color(pixel, google_colors["light_empty"]):  # Top right of the board
                    top_left = (x, y)
                    break
        elif not box_one_bottom_right:
            pixel = im.getpixel((top_left[0], y))
            if near_same_color(pixel, google_colors["dark_empty"]):  # Next box has started
                for x in range(top_left[0], im.width):  # Skip any x value to the left of the board
                    pixel = im.getpixel((x, y))
                    if near_same_color(pixel, google_colors["light_empty"]):  # Box down and right to top left
                        box_one_bottom_right = (x - 1, y - 1)
                        break
                if box_one_bottom_right is None:
                    return None
        else:
            pixel = im.getpixel((top_left[0], y))
            if not near_same_color(pixel, google_colors["light_empty"]) and not near_same_color(pixel, google_colors[
                    "dark_empty"]):
                # Bottom of the board is found, need to find bottom right now
                for x in range(top_left[0], im.width):
                    pixel = im.getpixel((x, y - 1))
                    if not near_same_color(pixel, google_colors["light_empty"]) and not near_same_color(pixel,
                                                                                                        google_colors[
                                                                                                            "dark_empty"]):
                        # Found the left edge on the bottom most pixel
                        bottom_right = (x - 1, y - 1)
                        break
    if not bottom_right:
        return None

    # Make sure to add + 1 because subtracting the 2 gives the distance rather than the total dimensions
    board_dimensions = (bottom_right[0] - top_left[0] + 1, bottom_right[1] - top_left[1] + 1)
    box_dimensions = (box_one_bottom_right[0] - top_left[0] + 1, box_one_bottom_right[1] - top_left[1] + 1)
    return GoogleBoard(top_left, board_dimensions, box_dimensions)


class GoogleBoard:
    def __init__(self, top_left, board_dimensions, box_dimensions):
        self.top_left = top_left
        self.dimensions = board_dimensions
        self.box_dimensions = box_dimensions
        self.boxes_horizontal = int(self.dimensions[0] / self.box_dimensions[0])
        self.boxes_vertical = int(self.dimensions[1] / self.box_dimensions[1])

        # Get virtual board
        self.virtual_board = virtual_board.Board(self.boxes_horizontal, self.boxes_vertical)
        self.update()

    def box_count(self):
        return self.boxes_vertical * self.boxes_horizontal

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

    def tile_value(self, x, y, screen):
        positions = self.tile_range(x, y)
        mid_pixel = screen.getpixel(self.get_mouse_position(x, y))
        tile_area = screen.crop((positions[0][0], positions[1][0], positions[0][1], positions[1][1]))
        unique_colors = tile_area.getcolors(tile_area.size[0]*tile_area.size[1])
        for c in unique_colors:
            color = c[1]
            if near_same_color(color, google_colors["flag"], 10):
                return -1
            elif near_same_color(color, google_colors["one"], 10):
                return 1
            elif near_same_color(color, google_colors["two"], 10):
                return 2
            elif near_same_color(color, google_colors["three"], 10):
                return 3
            elif near_same_color(color, google_colors["four"], 10):
                return 4

        if near_same_color(mid_pixel, google_colors["light_open"]) or near_same_color(mid_pixel,
                                                                                       google_colors["dark_open"]):
            return 0
        return None

    def update(self):
        screen = pyautogui.screenshot()
        tiles = self.virtual_board.get_empty_tiles()
        for tile in tiles:
            self.virtual_board.set_value(tile[0], tile[1], self.tile_value(tile[0], tile[1], screen))

    def game_over(self):
        screen = pyautogui.screenshot()
        for y in range(self.boxes_vertical):
            for x in range(self.boxes_horizontal):
                pos = self.get_mouse_position(x, y)
                pixel = screen.getpixel(pos)
                if near_same_color(pixel, google_colors["results"], 10):
                    return True


google_colors = {
    "light_empty": (170, 215, 81),
    "dark_empty": (162, 209, 73),
    "light_open": (224, 195, 163),
    "dark_open": (211, 185, 157),
    "border": (126, 164, 53),
    "flag": (242, 54, 7),
    "results": (77, 193, 249),
    # The colors are gradients, but as long as the color shows on the square its a number
    "one": (25, 118, 210),
    "two": (55, 141, 59),
    "three": (211, 47, 47),
    "four": (119, 16, 162)
}
