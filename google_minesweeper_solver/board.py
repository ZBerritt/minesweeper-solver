# Virtual minesweeper board derived from the browser for simulating and calculations
import math


class Board:

    def __init__(self, horizontal_tiles, vertical_tiles, number_of_mines):
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles
        self.number_of_mines = number_of_mines
        self.board = [[None]*horizontal_tiles]*vertical_tiles
        self.populated = False

    def populate_board(self):
        pass

    def print_board(self):
        board = self.board
        string = ""
        for row in board:
            string += "\n"
            for i in range(1 + self.horizontal_tiles * 4):
                string += "-"
            string += "\n|"
            for point in row:
                if point == 0:
                    char = " "
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




