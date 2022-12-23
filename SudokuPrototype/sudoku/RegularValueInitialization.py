from typing import NoReturn, List
from random import shuffle
from sudoku.RegularSudoku import RegularSudoku

def __next(rowIndex: int, colIndex: int, puzzle: RegularSudoku) -> (int, int):
    colIndex += 1

    if colIndex == puzzle.length:
        rowIndex += 1
        colIndex = 0

    return (rowIndex, colIndex)

def __value_initialize_helper2(puzzle: RegularSudoku, legalValues: List[str], rowIndex: int, colIndex: int) -> bool:
    (rowIndex, colIndex) = __next(rowIndex, colIndex, puzzle)

    return puzzle.length == rowIndex and __value_initialize_helper1(puzzle, legalValues, rowIndex, colIndex)

def __value_initialize_helper1(puzzle: RegularSudoku, legalValues: List[str], rowIndex: int, colIndex: int) -> bool:
    shuffle(legalValues)

    for value in legalValues:
        if puzzle.safe(rowIndex, colIndex, value):
            puzzle.set(rowIndex, colIndex, value)

            if __value_initialize_helper2(puzzle, legalValues, rowIndex, colIndex):
                return True

            puzzle.delete(rowIndex, colIndex)

    return False

def _value_initialize(puzzle: RegularSudoku, legalValues: List[str]) -> NoReturn:
    __value_initialize_helper1(puzzle, legalValues, 0, 0)
