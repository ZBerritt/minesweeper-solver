# Minesweeper Solver
A CLI bot for beating Minesweeper

## Supported
- Google Minesweeper
- Windows XP (W.I.P.)

## Usage
Simply run the executable in the terminal `./minesweeper_solver [game]`

## Flags
| **Flag**             | **Description**                                                       | **Default**                |
|----------------------|-----------------------------------------------------------------------|----------------------------|
| --delay (-d) [DELAY] | Delay in seconds for bot to execute next move                         | _Depends on the game type_ |
| --no-guess (-ng)     | Disables guessing, the bot will stop if no certain moves are detected | False                      |
| --flags (-f)         | Enables flagging possible mines                                       | False                      |
| --verbose (-v)       | Enable verbose logging                                                | False                      |
| --print-board (-p)   | Prints the current board after every set of moves                     | False                      |

## Building
Minesweeper Solver uses Nuitka to build for performance purposes **Nuitka currently only supports up to Python 3.11**

1. Clone the git repository `git clone https://github.com/ZBerritt/minesweeper-solver.git`
2. Move into the directory `cd minesweeper-solver`
3. Install Requirements using `pip install -r requirements.txt`
4. Run the build script `python buildscript.py`. This may prompt you to install a C compiler if you don't have one.
5. Run the executable file: `output/minesweeper-solver.exe`



