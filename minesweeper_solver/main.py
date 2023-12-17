import argparse
import logging
import os
import sys
import time
import threading
import keyboard
from games.game import Game, Status
from board.ai import Action, get_next_moves
from games.game_factory import game_factory

def solver():
    args = parse_args()
    logging.basicConfig(level=args.loglevel, format="%(message)s")

    logging.info("Scanning for Minesweeper board...")
    game = game_factory(args.type)

    if game is None:
        print("No board could be found! Make sure the app is all on screen.")
        return

    print(f"{game.name} board detected! Beginning solver...")
    print("Note: To escape, press ESC")

    game_status = do_move(game, flags=args.flags, delay=args.delay, no_guess=args.no_guess)

    while game_status == Status.INPROGRESS:
        game_status = do_move(game, flags=args.flags, delay=args.delay, no_guess=args.no_guess)

    game.board.print()
    if game_status == Status.LOST:
        print("Game Over...")
    elif game_status == Status.WON:
        print("I win!")
    elif game_status == Status.STUCK:
        print("No more moves can be found...")

def do_move(game: Game, flags=False, delay=None, no_guess=False) -> Status:
    time.sleep(delay if delay is not None else game.delay)
    
    game.update()
    logging.info("Getting next moves...")
    moves =  get_next_moves(game.board, no_guess) 
    if not moves:
        return Status.STUCK
    
    for move in moves:
        board_x, board_y, action = move
        logging.info(f"({board_x}, {board_y}) - {'Mine' if action == Action.FLAG else 'Safe'}")
        if action == Action.CLICK:
            game.click_action(board_x, board_y)
        elif action == Action.FLAG and flags:
            game.flag_action(board_x, board_y)
            
    return game.status()

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="Minesweeper Solver",
        description="A bot for solving the game minesweeper"
    )
    parser.add_argument("type", help="The Minesweeper game type to solve", choices=["google", "virtual-easy", "virtual-medium", "virtual-hard"])
    parser.add_argument("-d", "--delay", help="Override delay in seconds before each move (WARNING: Can break on certain games)", type=int)
    parser.add_argument("-ng", "--no-guess", help="Disable any guessing from the AI, only 100%% sure moves are executed", action="store_true")
    parser.add_argument("-f", "--flags", help="Send command to flag detected mines", action="store_true")
    parser.add_argument("-v", "--verbose", help="Show extra logging", action="store_const", dest="loglevel", const=logging.INFO)
    return parser.parse_args()

def on_escape_pressed(e):
    if e.name == 'esc':
        print("Exiting solver...")
        os._exit(1)

if __name__ == "__main__":
    keyboard.hook(on_escape_pressed)
    main_thread = threading.Thread(target=solver)
    main_thread.start()
    main_thread.join()
