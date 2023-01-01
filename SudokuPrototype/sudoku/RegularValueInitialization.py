from typing import NoReturn, List, Dict, Tuple
from random import shuffle
from copy import copy
from sudoku.RegularSudoku import RegularSudoku

def __next(rowIndex: int, colIndex: int, puzzle: RegularSudoku) -> (int, int):
    colIndex += 1

    if colIndex == puzzle.length:
        rowIndex += 1
        colIndex = 0

    return (rowIndex, colIndex)

def __value_initialize_helper(
        puzzle: RegularSudoku,
        valueDict: Dict[Tuple[int, int], List[str]],
        rowIndex: int,
        colIndex: int
) -> bool:
    if rowIndex == puzzle.length:
        return True

    legalValues = valueDict[(rowIndex, colIndex)]
    (nextRowIndex, nextColIndex) = __next(rowIndex, colIndex, puzzle)

    for value in legalValues:
        if puzzle.is_safe(rowIndex, colIndex, value):
            puzzle.set(rowIndex, colIndex, value)

            if __value_initialize_helper(puzzle, valueDict, nextRowIndex, nextColIndex):
                return True

            puzzle.delete(rowIndex, colIndex)

    return False

def __shuffle_values(puzzle: RegularSudoku, legalValues: List[str]) -> Dict[Tuple[int, int], List[str]]:
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

    __value_initialize_helper(puzzle, valueDict, 0, 0)
