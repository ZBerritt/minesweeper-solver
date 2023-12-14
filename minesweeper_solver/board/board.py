# Virtual minesweeper board derived from the browser for simulating and calculations
from dataclasses import dataclass

FLAGGED = -1
@dataclass
class Tile:
    x: int
    y: int
    value: int

class Board:
    def __init__(self, horizontal_tiles: int, vertical_tiles: int):
        # Generates empty board
        self.horizontal_tiles = horizontal_tiles
        self.vertical_tiles = vertical_tiles
        self.board = [[Tile(x=i, y=j, value=None) for i in range(horizontal_tiles)] for j in range(vertical_tiles)]

    def populate_board(self, values: list[list[int]]):
        for y, row in enumerate(values):
            for x, value in enumerate(row):
                self.set_value(x, y, Tile(value))

    def get_space(self, x: int, y: int) -> Tile:
        return self.board[y][x]

    def set_value(self, x: int, y: int, value: int) -> bool:
        if self.board[y][x].value != None:
            return False
        self.board[y][x].value = value
        return True

    def get_surrounding_tiles(self, tile: Tile) -> list[Tile]:
        tiles = []
        positions = [
            (tile.x - 1, tile.y - 1),  # Above-Left
            (tile.x, tile.y - 1),      # Above
            (tile.x + 1, tile.y - 1),  # Above-Right
            (tile.x + 1, tile.y),      # Right
            (tile.x + 1, tile.y + 1),  # Bottom-Right
            (tile.x, tile.y + 1),      # Bottom
            (tile.x - 1, tile.y + 1),  # Bottom-Left
            (tile.x - 1, tile.y),      # Left
        ]
        for pos in positions:
            px, py = pos
            if 0 <= px < self.horizontal_tiles and 0 <= py < self.vertical_tiles:
                tiles.append(self.get_space(px, py))
        return tiles

    def get_all_tiles(self) -> list[Tile]:
        return [self.get_space(x, y) for y in range(self.vertical_tiles) for x in range(self.horizontal_tiles)]

    def get_undiscovered_tiles(self) -> list[Tile]:
        return [t for t in self.get_all_tiles() if t.value is None]
    
    def get_discovered_tiles(self) -> list[Tile]:
        return [t for t in self.get_all_tiles() if t.value is not None]

    # Tiles that border any undiscovered tile.
    def get_border_tiles(self) -> list[Tile]:
        tiles = []
        for tile in self.get_discovered_tiles():
            if tile.value is None or tile.value == FLAGGED:
                continue
            surrounding = self.get_surrounding_tiles(tile)
            for adj_tile in surrounding:
                if adj_tile.value is None:
                    tiles.append(tile)
                    break
        return tiles

    # Undiscovered tiles that border a known tile
    def get_undiscovered_borders(self) -> list[Tile]:
        tiles = []
        all_tiles = self.get_undiscovered_tiles()
        for tile in all_tiles:
            if tile.value is not None:
                continue
            surrounding = self.get_surrounding_tiles(tile)
            for adj_tile in surrounding:
                if adj_tile.value is not None \
                        and adj_tile.value != FLAGGED:
                    tiles.append(tile)
                    break
        return tiles

    # Remaining # of mines surrounding a space
    def remaining_nearby_mines(self, tile: Tile) -> int:
        if tile.value == 0:
            return 0
        surrounding = self.get_surrounding_tiles(tile)
        return tile.value - len([m for m in surrounding if m.value == FLAGGED])

    def print(self):
        for row in self.board:
            for tile in row:
                print("-" if tile.value is None else "F" if tile.value == -1 else tile.value, end=" ")    
            print()