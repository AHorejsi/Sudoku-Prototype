from typing import NoReturn
from sudoku.RegularSudoku import RegularSudoku
from sudoku.RegularSolver import _has_unique_solution

def __next_snake(rowIndex: int, colIndex: int, puzzle: RegularSudoku) -> (int, int):
    if 0 == rowIndex % 2:
        colIndex += 1

        if colIndex == puzzle.length:
            rowIndex += 1
            colIndex = 0
    else:
        colIndex -= 1

        if -1 == colIndex:
            rowIndex += 1
            colIndex = puzzle.length - 1

    return (rowIndex, colIndex)

def __adjust_for_difficulty_helper1(puzzle: RegularSudoku, rowIndex: int, colIndex: int) -> NoReturn:
    value = puzzle.get(rowIndex, colIndex)
    puzzle.delete(rowIndex, colIndex)

    (rowIndex, colIndex) = __next_snake(rowIndex, colIndex, puzzle)

    if _has_unique_solution(puzzle):
        __adjust_for_difficulty_helper1(puzzle, rowIndex, colIndex)
    else:
        puzzle.set(rowIndex, colIndex, value)
        __adjust_for_difficulty_helper1(puzzle, rowIndex, colIndex)

def _adjust_for_difficulty(puzzle: RegularSudoku) -> NoReturn:
    __adjust_for_difficulty_helper1(puzzle, 0, 0)