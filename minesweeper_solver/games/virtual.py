from dataclasses import dataclass
from games.game import Game, Status
import random

WIDTH = 20
HEIGHT = 20
MINES = 50

@dataclass
class VirtualTile:
    mine: bool
    clicked: bool

# Tile - (value: int, discovered: bool)
class VirtualBoard(Game):
    def __init__(self):
        super().__init__("Virtual", WIDTH, HEIGHT, 0)
        self.internal_board = []

    def update(self):
        for y, row in enumerate(self.internal_board):
            for x, tile in enumerate(row):
                if tile.clicked and not tile.mine:
                    self.board.set_value(x, y, self.tile_value(x, y))
                        
    
    def status(self) -> Status:
        if (any(self.internal_board[y][x].mine and self.internal_board[y][x].clicked for x in range(WIDTH) for y in range(HEIGHT))):
            return Status.LOST
        if (any(not self.internal_board[y][x].mine and not self.internal_board[y][x].clicked for x in range(WIDTH) for y in range(HEIGHT))):
            return Status.INPROGRESS
        return Status.WON

    def get_board() -> Game:
        return VirtualBoard()
    
    def flag_action(self, x, y):
        pass
    
    def click_action(self, x, y):
        if not self.internal_board:
            self.create_board(x, y)
            
        stack = [(x, y)]
        visited = set()
        while stack:
            curr_x, curr_y = stack.pop()
            
            if (curr_x, curr_y) in visited:
                continue
            
            visited.add((curr_x, curr_y))
        
            self.internal_board[curr_y][curr_x].clicked = True
            if self.internal_board[curr_y][curr_x].mine:
                return
            value = self.tile_value(curr_x, curr_y)
            
            if value == 0:
                surrounding = self.get_surrounding_tiles(x, y)
                stack.extend(surrounding)

    def create_board(self, start_x, start_y):
        board_coordinates = [(x, y) for x in range(WIDTH) for y in range(HEIGHT) 
                             if (x, y) != (start_x, start_y) and (x, y) not in self.get_surrounding_tiles(start_x, start_y)]
        mine_coordinates = random.sample(board_coordinates, MINES)
        self.internal_board = [[VirtualTile((x, y) in mine_coordinates, False)
                                for x in range(WIDTH)] for y in range(HEIGHT)]

    def tile_value(self, x, y) -> int:
        return sum(1 for coords in self.get_surrounding_tiles(x, y) 
                              if self.internal_board[coords[1]][coords[0]].mine)
        
    def get_surrounding_tiles(self, x, y) -> list[tuple[int, int]]:
        tiles = []
        positions = [
            (x - 1, y - 1),  # Above-Left
            (x, y - 1),      # Above
            (x + 1, y - 1),  # Above-Right
            (x + 1, y),      # Right
            (x + 1, y + 1),  # Bottom-Right
            (x, y + 1),      # Bottom
            (x - 1, y + 1),  # Bottom-Left
            (x - 1, y),      # Left
        ]
        for pos in positions:
            px, py = pos
            if 0 <= px < WIDTH and 0 <= py < HEIGHT:
                tiles.append((px, py))
        return tiles