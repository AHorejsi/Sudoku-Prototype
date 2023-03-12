from typing import List
from sudoku.ValueInitialization import _initialize_values
from sudoku.RegularDifficultyAdjustment import _adjust_for_difficulty_regular
from sudoku.RegularShuffler import _shuffle_board_regular
from sudoku.Cell import _Cell
from sudoku.RegularSudoku import _RegularSafety, RegularInfo, RegularSudoku

def __make_cells(length: int) -> List[_Cell]:
    """
    Creates the 1 dimensional list of cells to be used for the sudoku board. Shall only be called from within the
    Generation.py file
    :param length: the number of rows and columns to be used for the sudoku board
    :return: A list of cells that will be used to represent the sudoku board's values
    """

    cells = []

    for _ in range(length * length):
        new = _Cell()
        cells.append(new)

    return cells

def generate_regular(info: RegularInfo) -> RegularSudoku:
    """
    Generates a regular sudoku with the provided info parameters specifying the criteria to be used when making
    the sudoku board
    :param info: Contains all the parameters needed for generating the sudoku board in accordance with its
        intended dimensions and difficulty level
    :return: A sudoku board for someone to play/solve
    """

    legalValues = list(info.legal)
    length = info.length

    table = __make_cells(length)
    safety = _RegularSafety(length)

    puzzle = RegularSudoku(info, table, safety)

    _initialize_values(puzzle, legalValues)
    #_adjust_for_difficulty_regular(puzzle)
    _shuffle_board_regular(puzzle)

    puzzle._finalize()

    return puzzle
