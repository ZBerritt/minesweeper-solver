from games.game import Game, Status
from board.board import FLAGGED

# Tile - (value: int, discovered: bool)
class VirtualBoard(Game):
    def __init__(self):
        super().__init__("Virtual", 20, 20, 0)
        self.internal_board = [[None for i in range(20)] for j in range(20)]
        self.exploded = False

    def update(self):
        for y, row in self.internal_board:
            for x, tile in row:
                if tile[1]:
                    self.board.set_value(x, y, self.internal_board[y][x])
    
    def status(self) -> Status:
        if self.exploded:
            return Status.LOST
        for y, row in self.internal_board:
            for x, tile in row:
                if tile != self.board.get_space(x, y).value:
                    return Status.INPROGRESS
        return Status.WON

    def get_board(self) -> Game:
        pass
    
    def flag_action(self, x, y):
        pass
    
    def click_action(self, x, y):
        if self.internal_board[y][x][0] == -1:
            self.exploded = True
        else:
            self.internal_board[y][x][1] == True