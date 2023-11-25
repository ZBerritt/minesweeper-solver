from typing import Optional
from games.game import Game
from games.google import GoogleBoard

def game_factory(type: str) -> Optional[Game]:
    if type == "google":
        return GoogleBoard.get_board()
    return None