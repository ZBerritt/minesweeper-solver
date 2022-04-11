import time

import pyautogui

from google_minesweeper_solver import ai
from google_minesweeper_solver.games.google import get_board


def do_move(board):
    done = board.game_over()
    if done:
        return print("Game Over.")
    virtual_board = board.virtual_board
    virtual_board.solve_tiles()
    moves = ai.get_next_move(board.virtual_board)
    if moves is None:
        return print("No more moves can be found...")
    for move in moves:
        x, y, action = move
        pyautogui.moveTo(board.get_mouse_position(x, y))
        action_name = ""
        if action == 0:
            action_name = "Flag"
        elif action == 1:
            action_name = "Click"
        print(f"({x}, {y}) - {action_name}")
        if action == 0:
            pyautogui.click(button="right")
            virtual_board.get_space(move[0], move[1]).value = -1  # Change the value to a mine, no need to rescan
        elif action == 1:
            pyautogui.click(button="left")
            pyautogui.moveTo(1, 1)
    if moves[0][2] == 1:  # Weird way to determine if the board needs reloading
        time.sleep(1)  # Google's animations make it hard to detect updates at an instant
        board.update()
    do_move(board)


if __name__ == "__main__":
    google_board = get_board()
    if google_board is None:
        print("No board could be found! Make sure the app is all on screen.")
    else:
        do_move(google_board)
