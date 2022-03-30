import time

import pyautogui

from google_minesweeper_solver import ai
from google_minesweeper_solver.games.google import get_board


def do_move(board):
    virtual_board = board.virtual_board
    virtual_board.solve_tiles()
    move = ai.get_next_move(board.virtual_board)
    pyautogui.moveTo(board.get_mouse_position(move.x, move.y))
    action_name = ""
    if move.action == 0:
        action_name = "Flag"
    elif move.action == 1:
        action_name = "Click"
    print("({}, {}) - {}".format(move.x, move.y, action_name))
    if move.action == 0:
        pyautogui.click(button="right")
        virtual_board.get_space(move.x, move.y).value = -1  # Change the value to a mine, no need to rescan
    elif move.action == 1:
        pyautogui.click(button="left")
        pyautogui.moveTo(1, 1)
        time.sleep(.25)
        board.update()
    do_move(board)


if __name__ == "__main__":
    google_board = get_board()
    if google_board is None:
        print("No board could be found! Make sure the app is all on screen.")
    else:
        do_move(google_board)
