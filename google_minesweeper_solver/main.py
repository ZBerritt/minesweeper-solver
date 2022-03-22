from time import sleep

from virtual_board import Board
import pyautogui
from google_minesweeper_solver.games.google import get_board


def main():
    board = get_board()
    print("Script Done!")


if __name__ == "__main__":
    main()
