import pyautogui

from google_minesweeper_solver import ai
from google_minesweeper_solver.games.google import get_board


def main():
    board = get_board()
    if board is None:
        return print("No board could be found!")
    move = ai.get_next_move(board.virtual_board)
    pyautogui.moveTo(board.get_mouse_position(move.x, move.y))
    if move.action == 0:
        pyautogui.click(button="right")
    elif move.action == 1:
        pyautogui.click(button="left")
    print("({}, {}) - {}".format(move.x, move.y, move.action))
    print("Script Done!")


if __name__ == "__main__":
    main()
