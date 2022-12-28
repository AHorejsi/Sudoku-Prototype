from typing import NoReturn, List, Dict
from random import shuffle
from copy import copy
from sudoku.RegularSudoku import RegularSudoku

def __next(rowIndex: int, colIndex: int, puzzle: RegularSudoku) -> (int, int):
    colIndex += 1

    if colIndex == puzzle.length:
        rowIndex += 1
        colIndex = 0

    return (rowIndex, colIndex)

def __value_initialize_helper2(
        puzzle: RegularSudoku,
        valueDict: Dict[(int, int), List[str]],
        rowIndex: int,
        colIndex: int
) -> bool:
    (rowIndex, colIndex) = __next(rowIndex, colIndex, puzzle)

    return puzzle.length == rowIndex or __value_initialize_helper1(puzzle, valueDict, rowIndex, colIndex)

def __value_initialize_helper1(
        puzzle: RegularSudoku,
        valueDict: Dict[(int, int), List[str]],
        rowIndex: int,
        colIndex: int
) -> bool:
    legalValues = valueDict[(rowIndex, colIndex)]

    for value in legalValues:
        if puzzle.is_safe(rowIndex, colIndex, value):
            puzzle.set(rowIndex, colIndex, value)

            if __value_initialize_helper2(puzzle, valueDict, rowIndex, colIndex):
                return True

            puzzle.delete(rowIndex, colIndex)

    return False

def __shuffle_values(puzzle: RegularSudoku, legalValues: List[str]) -> Dict[(int, int), List[str]]:
    length = puzzle.length
    valueDict = {}

    for rowIndex in range(length):
        for colIndex in range(length):
            legalValuesCopy = copy(legalValues)
            shuffle(legalValuesCopy)

            valueDict[(rowIndex, colIndex)] = legalValuesCopy

    return valueDict

def _value_initialize_regular(puzzle: RegularSudoku, legalValues: List[str]) -> NoReturn:
    valueDict = __shuffle_values(puzzle, legalValues)
    __value_initialize_helper1(puzzle, valueDict, 0, 0)
