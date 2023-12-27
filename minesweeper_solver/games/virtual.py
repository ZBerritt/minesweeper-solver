import random
from dataclasses import dataclass
from games.game import Game, Status
from utils.helpers import surrounding_tiles

difficulties = {
    "easy": {
        "width": 10,
        "height": 10,
        "mines": 10
    },
    "medium": {
        "width": 15,
        "height": 15,
        "mines": 40
    },
    "hard": {
        "width": 20,
        "height": 20,
        "mines": 100
    }
}

@dataclass
class VirtualTile:
    mine: bool
    clicked: bool

# Tile - (value: int, discovered: bool)
class VirtualBoard(Game):
    def __init__(self, difficulty: str):
        selected = difficulties[difficulty]
        super().__init__("Virtual", selected["width"], selected["height"], 0)
        self.mines = selected["mines"]
        self.internal_board = []

    def update(self):
        for y, row in enumerate(self.internal_board):
            for x, tile in enumerate(row):
                if tile.clicked and not tile.mine:
                    value = self.tile_value(x, y)
                    self.board.set_value(x, y, value)
                        
    
    def status(self) -> Status:
        clicked_mine = any(tile.mine and tile.clicked for row in self.internal_board for tile in row)
        unclicked_safe_tile = any(not tile.mine and not tile.clicked for row in self.internal_board for tile in row)
        
        if clicked_mine:
            return Status.LOST
        elif unclicked_safe_tile:
            return Status.INPROGRESS
        else:
            return Status.WON

    def get_board(difficulty: str) -> Game:
        return VirtualBoard(difficulty)
    
    def flag_action(self, x, y):
        pass
    
    def click_action(self, x: int, y: int):
        if not self.internal_board:
            self.create_board(x, y)
            
        stack = [(x, y)]
        visited = set()
        while stack:
            curr_x, curr_y = stack.pop()
            if (curr_x, curr_y) in visited:
                continue
            visited.add((curr_x, curr_y))
            
            tile = self.internal_board[curr_y][curr_x]
            tile.clicked = True
            
            value = self.tile_value(curr_x, curr_y)
            if value == 0 and not tile.mine:
                surrounding = self.get_surrounding_tiles(curr_x, curr_y)
                stack.extend(surrounding)

    def create_board(self, start_x, start_y):
        illegal_tiles = self.get_surrounding_tiles(start_x, start_y) + [(start_x, start_y)]
        board_coordinates = [(x, y) for x in range(self.boxes_horizontal) for y in range(self.boxes_vertical)]
        possible_mine_coordinates = [coords for coords in board_coordinates if coords not in illegal_tiles]
        mine_coordinates = random.sample(possible_mine_coordinates, self.mines)
        self.internal_board = [[VirtualTile((x, y) in mine_coordinates, False)
                                for x in range(self.boxes_horizontal)] for y in range(self.boxes_vertical)]

    def tile_value(self, x: int, y: int) -> int:
        return sum(1 for coords in self.get_surrounding_tiles(x, y) 
                              if self.internal_board[coords[1]][coords[0]].mine)
        
    def get_surrounding_tiles(self, x: int, y: int) -> list[tuple[int, int]]:
        return surrounding_tiles(x, y, self.boxes_horizontal, self.boxes_vertical, lambda x, y: (x, y))