from typing import Optional
from games.game import Game
from games.google import GoogleBoard
from games.virtual import VirtualBoard

def game_factory(type: str) -> Optional[Game]:
    if type == "google":
        return GoogleBoard.get_board()
    if type == "virtual-easy":
        return VirtualBoard.get_board("easy")
    if type == "virtual-medium":
        return VirtualBoard.get_board("medium")
    if type == "virtual-hard":
        return VirtualBoard.get_board("hard")
    return None