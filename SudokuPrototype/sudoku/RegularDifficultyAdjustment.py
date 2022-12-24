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

def __decide_lower_bound_on_units(puzzle: RegularSudoku) -> int:
    return round(puzzle.length * (puzzle.lower_bound_of_givens_per_unit / 100))

def _adjust_for_difficulty(puzzle: RegularSudoku) -> NoReturn:
    amountOfGivens = __decide_amount_of_givens(puzzle)
    lowerBoundOnUnits = __decide_lower_bound_on_units(puzzle)
