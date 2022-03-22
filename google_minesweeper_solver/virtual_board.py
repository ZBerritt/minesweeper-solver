# Virtual minesweeper board derived from the browser for simulating and calculations
import math


class Board:

    def __init__(self, horizontal_tiles, vertical_tiles):
        self.board = None
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles

    def populate_board(self, values):
        self.board = []
        row_num = -1
        for row in values:
            row_num += 1
            self.board.append([])
            for value in row:
                self.board[row_num].append(Tile(value))

    def get_space(self, x, y):
        return self.board[y][x]


class Tile:
    def __init__(self, value):
        """
        Values:
        None: Undiscovered
        -1: Flagged Mine
        0: Empty tile
        1-8: Numbered tile
        """
        self.value = value
        self.solved = False
