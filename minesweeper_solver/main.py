import time

import pyautogui

from minesweeper_solver import ai
from minesweeper_solver.games import google


def do_move(board, first=False):
    # Test for any end conditions
    end_condition = board.game_over()
    if end_condition == 1:
        return print("Game Over...")
    elif end_condition == 2:
        return print("I win!")

    # Move Setup
    virtual_board = board.virtual_board
    virtual_board.solve_tiles()  # Speed up the algorithm by ignoring tiles that don't matter

    # Execute next move
    moves = ai.get_next_moves(board.virtual_board, first)
    if moves is None:
        return print("No more moves can be found...")
    for move in moves:
        x, y, action = move
        print(f"({x}, {y}) - {'Flag' if action == 0 else 'Click'}")
        pyautogui.moveTo(board.get_mouse_position(x, y))
        button = "right" if action == 0 else "left";
        pyautogui.click(button=button)

    # Cleanup & Updates
    pyautogui.moveTo(1, 1)  # Move the mouse out of the way so the detection algorithm works fine
    time.sleep(board.move_delay / 1000)  # Google's animations make it hard to detect updates at an instant
    board.update()

    # Recursion
    do_move(board)


def get_board():
    # TODO - Make a faster method for getting the board (idk man)
    # Google
    board = google.get_board()
    if board:
        return board


if __name__ == "__main__":
    print("Scanning for Minesweeper boards...")
    m_board = get_board()  # Automatically gets the correct board type
    if m_board is None:
        print("No board could be found! Make sure the app is all on screen.")
    else:
        print("{0} board detected! Beginning solver.".format(m_board.name))
        do_move(m_board, True)
