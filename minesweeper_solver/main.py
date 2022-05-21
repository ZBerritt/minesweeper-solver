import time

import pyautogui

from minesweeper_solver import ai
from minesweeper_solver.games.google import get_board

SECONDS_TO_RELOAD = 2


def do_move(board, first=False):
    done = board.game_over()
    if done:
        return print("Game Over.")
    virtual_board = board.virtual_board
    virtual_board.solve_tiles()
    moves = ai.get_next_moves(board.virtual_board, first)
    if moves is None:
        return print("No more moves can be found...")
    for move in moves:
        x, y, action = move
        pyautogui.moveTo(board.get_mouse_position(x, y))
        print(f"({x}, {y}) - {'Flag' if action == 0 else 'Click'}")
        if action == 0:
            pyautogui.click(button="right")
        elif action == 1:
            pyautogui.click(button="left")
    pyautogui.moveTo(1, 1)  # Move the mouse out of the way so the detection algorithm works fine
    time.sleep(SECONDS_TO_RELOAD)  # Google's animations make it hard to detect updates at an instant
    board.update()
    do_move(board)


if __name__ == "__main__":
    google_board = get_board()
    if google_board is None:
        print("No board could be found! Make sure the app is all on screen.")
    else:
        do_move(google_board, True)
