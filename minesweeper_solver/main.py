import argparse
import time
import pyautogui
from games.game import Game
from board.ai import Action, get_next_moves
from games.game_factory import game_factory

MAX_RETRIES = 3

def solver():
    args = parse_args()

    print("Scanning for Minesweeper board...")
    game = game_factory(args.type)

    if game is None:
        print("No board could be found! Make sure the app is all on screen.")
        return

    print(f"{game.name} board detected! Beginning solver.")
    print("Note: To escape, move your cursor to the top-left corner of your screen")

    game_status = do_move(game, flags=args.flags, verbose=args.verbose, delay=args.delay)

    while game_status == 0:
        game_status = do_move(game, flags=args.flags, verbose=args.verbose, delay=args.delay)

    if game_status == 1:
        print("Game Over...")
    elif game_status == 2:
        print("I win!")
    elif game_status == 3:
        print("No more moves can be found...")

def do_move(game: Game, flags=False, verbose=False, delay=0) -> int:
    # Move Setup
    virtual_board = game.virtual_board
    virtual_board.solve_tiles()

    # Execute next move
    moves = None
    tries = 0
    while not moves and tries < MAX_RETRIES:
        curr_delay = 1 if tries else  delay / 1000
        time.sleep(curr_delay)
        pyautogui.moveTo(1, 1)
        game.update()
        moves = get_next_moves(virtual_board)
        tries += 1
    if not moves:
        return 3
    for move in moves:
        board_x, board_y, action = move
        screen_x, screen_y = game.get_mouse_position(board_x, board_y)

        if verbose:
            print(f"({board_x}, {board_y}) - {'Mine' if action == Action.FLAG else 'Safe'}")
            
        if action == Action.CLICK:
            pyautogui.click(x=screen_x, y=screen_y, button="left")
        elif action == Action.FLAG:
            virtual_board.set_mine(board_x, board_y)
            if flags:
                pyautogui.click(x=screen_x, y=screen_y, button="right")
    return game.status()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Minesweeper Solver",
        description="A bot for solving the game minesweeper"
    )
    parser.add_argument("type", help="The Minesweeper game type", choices=["google"])
    parser.add_argument("-v", "--verbose", help="Show the logs of the solver", action="store_true")
    parser.add_argument("-f", "--flags", help="Flag mines", action="store_true")
    parser.add_argument("-d", "--delay", help="Delay in milliseconds before each next move (can help with boards with animations)", type=int, default=0)

    return parser.parse_args()

if __name__ == "__main__":
    solver()
