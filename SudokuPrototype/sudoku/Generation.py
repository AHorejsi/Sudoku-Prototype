from typing import List
from sudoku.RegularValueInitialization import _value_initialize_regular
from sudoku.RegularDifficultyAdjustment import _adjust_for_difficulty_regular
from sudoku.RegularShuffler import _shuffle_board_regular
from sudoku.Cell import _Cell
from sudoku.RegularSudoku import _RegularSafety, RegularInfo, RegularSudoku

def __make_cells(length: int) -> List[_Cell]:
    cells = []

    for _ in range(length * length):
        cells.append(_Cell(None, True))

    return cells

def generate_regular(info: RegularInfo) -> RegularSudoku:
    legalValues = list(info.dimensions.value["legal"])
    length = info.dimensions.value["length"]

    table = __make_cells(length)
    safety = _RegularSafety(length)

    puzzle = RegularSudoku(info, table, safety)

    _value_initialize_regular(puzzle, legalValues)
    _adjust_for_difficulty_regular(puzzle)
    _shuffle_board_regular(puzzle, legalValues)

    puzzle._finalize()

    return puzzle


