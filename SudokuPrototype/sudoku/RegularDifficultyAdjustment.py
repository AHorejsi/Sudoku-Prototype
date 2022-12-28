from random import randint
from typing import NoReturn
from sudoku.RegularSudoku import RegularSudoku
from sudoku.RegularSolver import _has_unique_solution

def __decide_amount_of_givens(puzzle: RegularSudoku) -> int:
    total = puzzle.length * puzzle.length
    upperBound = puzzle.upper_bound_of_givens
    lowerBound = puzzle.lower_bound_of_givens

    percent = randint(lowerBound, upperBound)
    amount = round(total * (percent / 100))

    return amount

def __decide_lower_bound_on_unit(puzzle: RegularSudoku) -> int:
    return round(puzzle.length * (puzzle.lower_bound_of_givens_per_unit / 100))

def __check_lower_bound(puzzle: RegularSudoku, rowIndex: int, colIndex: int, lowerBoundOfGivensOnUnit: int) -> bool:
    (rowWeight, colWeight, boxWeight) = puzzle._weight(rowIndex, colIndex)

    return rowWeight <= lowerBoundOfGivensOnUnit and \
            colWeight <= lowerBoundOfGivensOnUnit and \
            boxWeight <= lowerBoundOfGivensOnUnit


def __do_adjustment(puzzle: RegularSudoku, amountOfGivens: int, lowerBoundOfGivensOnUnit: int) -> NoReturn:
    length = puzzle.length
    valueCount = length * length

    for rowIndex1 in range(length):
        for colIndex1 in range(length):
            if __check_lower_bound(puzzle, rowIndex1, colIndex1, lowerBoundOfGivensOnUnit):
                rowIndex2 = length - rowIndex1 - 1
                colIndex2 = length - colIndex1 - 1

                value1 = puzzle.get(rowIndex1, colIndex1)
                value2 = puzzle.get(rowIndex2, colIndex2)

                puzzle.delete(rowIndex1, colIndex1)
                puzzle.delete(rowIndex2, colIndex2)

                valueCount -= 2

                if not _has_unique_solution(puzzle):
                    puzzle.set(rowIndex1, colIndex1, value1)
                    puzzle.set(rowIndex2, colIndex2, value2)

                    valueCount += 2

                if valueCount <= amountOfGivens:
                    return

def _adjust_for_difficulty_regular(puzzle: RegularSudoku) -> NoReturn:
    amountOfGivens = __decide_amount_of_givens(puzzle)
    lowerBoundOfGivensOnUnit = __decide_lower_bound_on_unit(puzzle)

    __do_adjustment(puzzle, amountOfGivens, lowerBoundOfGivensOnUnit)
