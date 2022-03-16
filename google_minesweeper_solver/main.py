from time import sleep

from virtual_board import Board
import pyautogui
from google_minesweeper_solver.games.google import get_board


def main():
    # currently just fun test functions
    board = get_board()
    print(board.boxes_horizontal())
    print(board.boxes_vertical())
    print(board.box_count())
    for y in range(board.boxes_vertical()):
        for x in range(board.boxes_horizontal()):
            sleep(.5)
            mp = board.get_mouse_position(x, y)
            pyautogui.moveTo(mp[0], mp[1])
    print("done")


if __name__ == "__main__":
    main()
