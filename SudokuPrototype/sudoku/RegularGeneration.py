from sudoku.RegularValueInitialization import _value_initialize
from sudoku.RegularDifficultyAdjustment import _adjust_for_difficulty
from sudoku.RegularShuffler import _shuffle_board
from sudoku.Cell import _Cell
from sudoku.SudokuInfo import SudokuInfo
from sudoku.RegularSudoku import RegularSudoku, __RegularSafety

def generate_regular(info: SudokuInfo) -> RegularSudoku:
    length = info.dimensions.value["length"]

    table = [_Cell(None, True)] * (length * length)
    safety = __RegularSafety(length)
    legalValues = list(info.dimensions.value["legal"])

    puzzle = RegularSudoku(info, table, safety)

    _value_initialize(puzzle, legalValues)
    _adjust_for_difficulty(puzzle)
    _shuffle_board(puzzle, legalValues)

    puzzle._finalize()

    return puzzle
