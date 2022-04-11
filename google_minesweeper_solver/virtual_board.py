# Virtual minesweeper board derived from the browser for simulating and calculations
from dataclasses import dataclass


class Board:

    def __init__(self, horizontal_tiles, vertical_tiles):
        # Generates empty board
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles
        self.board = [[Tile(None, False) for i in range(self.horizontal_tiles)] for i in range(self.vertical_tiles)]

    def populate_board(self, values):
        for y in range(len(values)):
            for x in range(len(values[y])):
                value = values[y][x]
                self.set_value(x, y, Tile(value))

    def get_space(self, x, y):
        return self.board[y][x]

    def set_value(self, x, y, value):
        self.board[y][x].set_value(value)  # Sets a new value without re-declaring the tile

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

    def get_all_tiles(self):
        tiles = []
        for y in range(self.vertical_tiles):
            for x in range(self.horizontal_tiles):
                tile = self.get_space(x, y)
                tiles.append((x, y, tile))
        return tiles

    def get_unsolved_tiles(self):
        return [t for t in self.get_all_tiles() if not t[2].solved]

    # Undiscovered, not empty
    def get_empty_tiles(self):
        return [t for t in self.get_all_tiles() if t[2].value is None]

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

    # Tiles that border any undiscovered tile. 
    # TODO - Might need another function to get undiscovered tiles that border numbered tiles
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


@dataclass
class Tile:
    """
    Values:
    None: Undiscovered
    -1: Flagged Mine
    0: Empty tile
    1-8: Numbered tile
    """
    value: int
    solved: bool  # True if all surrounding squares have a value other than None (discovered/flagged)

    def set_value(self, value):
        self.value = value
