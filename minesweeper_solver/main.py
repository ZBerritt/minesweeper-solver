import argparse
import time
import pyautogui
from games.game import Game
from board.ai import Action, get_next_moves
from games.game_factory import game_factory


def solver():
    args = parse_args()

    print("Scanning for Minesweeper board...")
    game = game_factory(args.type)

    if game is None:
        print("No board could be found! Make sure the app is all on screen.")
        return

    print(f"{game.name} board detected! Beginning solver.")
    print("Note: To escape, move your cursor to the top-left corner of your screen")

    game_status = do_move(game, flags=args.flags, verbose=args.verbose)

    while game_status == 0:
        game_status = do_move(game, flags=args.flags, verbose=args.verbose)

    if game_status == 1:
        print("Game Over...")
    elif game_status == 2:
        print("I win!")
    elif game_status == 3:
        print("No more moves can be found...")

def do_move(game: Game, flags=False, verbose=False) -> int:
    # Move Setup
    virtual_board = game.virtual_board
    virtual_board.solve_tiles()

    # Execute next move
    moves = get_next_moves(virtual_board)
    if not moves:
        return 3
    clicked = False
    for move in moves:
        x, y, action = move
        mouse_position = game.get_mouse_position(x, y)
        if verbose:
            print(f"({x}, {y}) - {'Mine' if action == 0 else 'Safe'}")
        if action == Action.CLICK:  # Safe
            pyautogui.moveTo(mouse_position)
            clicked = True
            pyautogui.click(button="left")
        else:  # Mine
            if flags:
                pyautogui.moveTo(mouse_position)
                clicked = True
                pyautogui.click(button="right")
            virtual_board.set_mine(x, y)  # Manually set the mine, solver ignores flags

    # Cleanup & Updates
    if clicked:
        pyautogui.moveTo(1, 1)  # Move the mouse out of the way so the detection algorithm works fine
        time.sleep(game.move_delay / 1000)  # Google's animations make it hard to detect updates at an instant
        game.update()

    # Recursion
    return game.game_over()

def parse_args():
    parser = argparse.ArgumentParser(
        prog="Minesweeper Solver",
        description="A bot for solving the game minesweeper"
    )
    parser.add_argument("type", help="The Minesweeper game type", choices=["google"])
    parser.add_argument("-v", "--verbose", help="Show the logs of the solver", action="store_true")
    parser.add_argument("-f", "--flags", help="Flag mines", action="store_true")

    return parser.parse_args()

if __name__ == "__main__":
    solver()
