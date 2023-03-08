from random import randint
from sudoku.StateError import StateError
from sudoku.RegularSudoku import RegularSudoku
from sudoku.RegularSolver import _has_unique_solution

def __decide_amount_of_givens(puzzle: RegularSudoku) -> int:
    total = puzzle.length * puzzle.length
    upperBound = puzzle.initial_upper_bound_of_givens
    lowerBound = puzzle.initial_lower_bound_of_givens

    percent = randint(lowerBound, upperBound)
    amount = round(total * (percent / 100))

    return amount

def __decide_lower_bound_on_unit(puzzle: RegularSudoku) -> int:
    return round(puzzle.length * (puzzle.initial_lower_bound_of_givens_per_unit / 100))

def __check_lower_bound(puzzle: RegularSudoku, rowIndex: int, colIndex: int, lowerBoundOfGivensOnUnit: int) -> bool:
    (rowGivenCount, colGivenCount, boxGivenCount) = puzzle._givens(rowIndex, colIndex)

    rowResult = rowGivenCount >= lowerBoundOfGivensOnUnit
    colResult = colGivenCount >= lowerBoundOfGivensOnUnit
    boxResult = boxGivenCount >= lowerBoundOfGivensOnUnit

    return rowResult and colResult and boxResult

def __try_remove(puzzle: RegularSudoku, rowIndex: int, colIndex: int, valueCount: int) -> int:
    value = puzzle.get(rowIndex, colIndex)

    puzzle.delete(rowIndex, colIndex)

    if _has_unique_solution(puzzle):
        return valueCount - 1
    else:
        puzzle.set(rowIndex, colIndex, value)

        return valueCount


def __do_adjustment(puzzle: RegularSudoku, amountOfGivens: int, lowerBoundOfGivensOnUnit: int):
    length = puzzle.length
    valueCount = length * length

    for rowIndex1 in range(length):
        for colIndex1 in range(length):
            if __check_lower_bound(puzzle, rowIndex1, colIndex1, lowerBoundOfGivensOnUnit):
                rowIndex2 = length - rowIndex1 - 1
                colIndex2 = length - colIndex1 - 1

                valueCount = __try_remove(puzzle, rowIndex1, colIndex1, valueCount)
                valueCount = __try_remove(puzzle, rowIndex2, colIndex2, valueCount)

                if valueCount <= amountOfGivens:
                    return

def _adjust_for_difficulty_regular(puzzle: RegularSudoku):
    amountOfGivens = __decide_amount_of_givens(puzzle)
    lowerBoundOfGivensOnUnit = __decide_lower_bound_on_unit(puzzle)

    __do_adjustment(puzzle, amountOfGivens, lowerBoundOfGivensOnUnit)

    if not puzzle.is_valid():
        raise StateError(f"Sudoku board must still be valid by this point\n{puzzle}")
    if puzzle.is_complete():
        raise StateError(f"Sudoku board must not be complete by this point\n{puzzle}")
