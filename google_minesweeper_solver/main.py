import time

import pyautogui

from google_minesweeper_solver import ai
from google_minesweeper_solver.games.google import get_board


def main():
    board = get_board()
    if board is None:
        return print("No board could be found!")
    do_move(board)


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
    print("({}, {}) - {}".format(move.x, move.y, move.action))
    if move.action == 0:
        pyautogui.click(button="right")
        virtual_board.get_space(move.x, move.y).value = -1  # Change the value to a mine, no need to rescan
    elif move.action == 1:
        pyautogui.click(button="left")
        pyautogui.moveTo(1, 1)
        virtual_board.populate_board(board.get_tile_values())
    time.sleep(.5)
    do_move(board)


if __name__ == "__main__":
    main()
