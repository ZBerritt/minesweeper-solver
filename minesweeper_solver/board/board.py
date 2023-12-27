# Virtual minesweeper board derived from the browser for simulating and calculations
from dataclasses import dataclass
from typing import Optional

from utils.helpers import surrounding_tiles

FLAGGED = -1
@dataclass
class Tile:
    x: int
    y: int
    value: Optional[int]

class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.board = [[Tile(x=i, y=j, value=None) for i in range(width)] for j in range(height)]

    def get_space(self, x: int, y: int) -> Tile:
        return self.board[y][x]

    def set_value(self, x: int, y: int, value: int):
        if self.board[y][x].value != None:
            return
        self.board[y][x].value = value

    def get_surrounding_tiles(self, tile: Tile) -> list[Tile]:
        return surrounding_tiles(tile.x, tile.y, self.width, self.height, lambda x, y: self.get_space(x, y))

    def get_all_tiles(self) -> list[Tile]:
        return [self.get_space(x, y) for y in range(self.height) for x in range(self.width)]

    def get_undiscovered_tiles(self) -> list[Tile]:
        return [t for t in self.get_all_tiles() if t.value is None]
    
    def get_discovered_tiles(self) -> list[Tile]:
        return [t for t in self.get_all_tiles() if t.value is not None]

    # Tiles that border any undiscovered tile.
    def get_border_tiles(self) -> list[Tile]:
        borders = []
        filtered_tiles = [tile for tile in self.get_discovered_tiles() if tile.value not in [None, FLAGGED]]
        for tile in filtered_tiles:
            surrounding = self.get_surrounding_tiles(tile)
            if any(adj_tile.value is None for adj_tile in surrounding):
                borders.append(tile)
        return borders

    # Undiscovered tiles that border a known tile
    def get_undiscovered_borders(self) -> list[Tile]:
        borders = []
        filtered_tiles = [tile for tile in self.get_undiscovered_tiles() if tile.value is None]
        for tile in filtered_tiles:
            surrounding = self.get_surrounding_tiles(tile)
            if any(adj_tile.value is not None and adj_tile.value != FLAGGED for adj_tile in surrounding):
                borders.append(tile)
        return borders

    # Remaining # of mines surrounding a space
    def remaining_nearby_mines(self, tile: Tile) -> int:
        if tile.value == 0:
            return 0
        surrounding = self.get_surrounding_tiles(tile)
        flagged_surrounding = len([m for m in surrounding if m.value == FLAGGED])
        return tile.value - flagged_surrounding if tile.value else flagged_surrounding

    def print(self):
        for row in self.board:
            for tile in row:
                print("-" if tile.value is None else "F" if tile.value == -1 else tile.value, end=" ")    
            print()