from sudoku.Cell import _Cell
from sudoku.RegularValueInitialization import _value_initialize_regular
from sudoku.RegularDifficultyAdjustment import _adjust_for_difficulty_regular
from sudoku.RegularShuffler import _shuffle_board_regular
from sudoku.RegularInfo import RegularInfo
from sudoku.RegularSafety import _RegularSafety
from sudoku.RegularSudoku import RegularSudoku

def generate_regular(info: RegularInfo) -> RegularSudoku:
    length = info.dimensions.value["length"]

    table = [_Cell(None, True)] * (length * length)
    safety = _RegularSafety(length)
    legalValues = list(info.dimensions.value["legal"])

    puzzle = RegularSudoku(info, table, safety)

    _value_initialize_regular(puzzle, legalValues)
    _adjust_for_difficulty_regular(puzzle)
    _shuffle_board_regular(puzzle, legalValues)

    puzzle._finalize()

    return puzzle
