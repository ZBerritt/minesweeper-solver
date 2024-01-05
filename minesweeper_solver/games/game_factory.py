from typing import Optional
from games.game import Game
from games.google import Google
from games.virtual import Virtual

def game_factory(type: str) -> Optional[Game]:
    if type == "google":
        return Google.create()
    if type == "virtual-easy":
        return Virtual.create("easy")
    if type == "virtual-medium":
        return Virtual.create("medium")
    if type == "virtual-hard":
        return Virtual.create("hard")
    return None