# Virtual minesweeper board derived from the browser for simulating and calculations
import math


class Board:

    def __init__(self, horizontal_tiles, vertical_tiles, number_of_mines):
        self.board = None
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles
        self.number_of_mines = number_of_mines

    def populate_board(self, board):
        self.board = board
        pass

    def print_board(self):
        board = self.board
        string = ""
        for row in board:
            string += "\n"
            for i in range(1 + self.horizontal_tiles * 4):
                string += "-"
            string += "\n|"
            for tile in row:
                point = tile.value
                if point == 0:
                    char = " "
                elif point == -1:
                    char = "f"
                elif point is None:
                    char = "*"
                else:
                    char = point
                string += " " + char + " |"
        string += "\n"
        for i in range(1 + self.horizontal_tiles * 4):
            string += "-"
        print(string)

    def get_space(self, x, y):
        return self.board[y][x]

    def get_space_number(self, x, y):
        pass

    def get_space_by_number(self, num):
        x = num % self.horizontal_tiles
        y = math.floor(num / self.horizontal_tiles)
        print("({}, {})".format(x, y))
        return self.get_space(x, y)


class Tile:
    def __init__(self, value, num, color):
        """
        Values:
        None: Undiscovered
        -1: Flagged Mine
        0: Empty tile
        1-8: Numbered tile
        """
        self.value = value
        self.solved = False
        self.number = num
        self.color = color  # Used only to map the squares
