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

    def get_surrounding_tiles(self, x, y):
        tiles = []
        if x != 0 and y != 0:
            tiles.append((x - 1, y - 1, self.get_space(x - 1, y - 1)))  # Above-Left
        if y != 0:
            tiles.append((x, y - 1, self.get_space(x, y - 1)))  # Above
        if x != self.horizontal_tiles - 1 and y != 0:
            tiles.append((x + 1, y - 1, self.get_space(x + 1, y - 1)))  # Above-Right
        if x != self.horizontal_tiles - 1:
            tiles.append((x + 1, y, self.get_space(x + 1, y)))  # Right
        if x != self.horizontal_tiles - 1 and y != self.vertical_tiles - 1:
            tiles.append((x + 1, y + 1, self.get_space(x + 1, y + 1)))  # Bottom-Right
        if y != self.vertical_tiles - 1:
            tiles.append((x, y + 1, self.get_space(x, y + 1)))  # Bottom
        if x != 0 and y != self.vertical_tiles - 1:
            tiles.append((x - 1, y + 1, self.get_space(x - 1, y + 1)))  # Bottom-Left
        if x != 0:
            tiles.append((x - 1, y, self.get_space(x - 1, y)))  # Left
        return tiles

    def get_unsolved_tiles(self):
        tiles = []
        x = -1
        y = -1
        for row in self.board:
            y += 1
            x = -1
            for tile in row:
                x += 1
                if not tile.solved:
                    tiles.append((x, y, tile))
        return tiles

    def get_empty_tiles(self):
        tiles = []
        for y in range(0, self.vertical_tiles):
            for x in range(0, self.horizontal_tiles):
                tile = self.get_space(x, y)
                if tile.value is None:
                    tiles.append((x, y, tile))
        return tiles

    def solve_tiles(self):
        unsolved_tiles = self.get_unsolved_tiles()
        for tile in unsolved_tiles:
            solved = True
            adj_tiles = self.get_surrounding_tiles(tile[0], tile[1])
            for adj_tile in adj_tiles:
                if adj_tile[2].value is None:
                    solved = False
                    break
            tile[2].solved = solved

    def get_border_tiles(self):
        tiles = []
        unsolved = self.get_unsolved_tiles()
        for tile in unsolved:
            if tile[2].value is None:
                continue
            surrounding = self.get_surrounding_tiles(tile[0], tile[1])
            for adj_tile in surrounding:
                if adj_tile[2].value is None:
                    tiles.append(tile)
                    break
        return tiles

    def remaining_nearby_mines(self, x, y):
        tile = self.get_space(x, y)
        if tile.value is None:
            return None
        if tile.value == 0:
            return 0
        surrounding = self.get_surrounding_tiles(x, y)
        return tile.value - len([m for m in surrounding if m[2].value == -1])


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
