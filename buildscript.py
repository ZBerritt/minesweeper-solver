# Build Script using Nuitka
import subprocess

PROGRAM_NAME="minesweeper-solver"
NAME = "Minesweeper Solver"
VERSION = "0.2.0"
MAIN_FILE_LOCATION = "minesweeper_solver/main.py"
NUITKA_COMMAND = "nuitka"

command = []
command.append(NUITKA_COMMAND)
command.append(f"--product-name={NAME}")
command.append(f"--file-version={VERSION}")
command.append(f"--output-filename={PROGRAM_NAME}")
command.append("--output-dir=output")
command.append("--standalone")
command.append(MAIN_FILE_LOCATION)

subprocess.run(command,  shell=True)

print("Build Complete")