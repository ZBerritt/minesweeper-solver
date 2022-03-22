from time import sleep

from virtual_board import Board
import pyautogui
from google_minesweeper_solver.games.google import get_board


def main():
    # currently just fun test functions
    board = get_board()
    if not board:
        return print("No board could be found")
    print(board.boxes_horizontal())
    print(board.boxes_vertical())
    print(board.box_count())
    colors = []
    for y in range(board.boxes_vertical()):
        for x in range(board.boxes_horizontal()):
            value = board.tile_value(x, y)
            if value is not None:
                pyautogui.moveTo(board.get_mouse_position(x, y))
                print(value)
    print("Script Done!")


if __name__ == "__main__":
    main()
