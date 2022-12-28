from typing import NoReturn, List, Dict
from random import randint, shuffle
from sudoku import RegularSudoku

def __horizontal_flip(puzzle: RegularSudoku) -> NoReturn:
    i = 0
    j = puzzle.length - 1

    while i < j:
        for row in range(puzzle.length):
            temp = puzzle.get(row, i)
            puzzle.set(row, i, puzzle.get(row, j))
            puzzle.set(row, j, temp)

        i += 1
        j -= 1

def __vertical_flip(puzzle: RegularSudoku) -> NoReturn:
    i = 0
    j = puzzle.length - 1

    while i < j:
        for col in range(puzzle.length):
            temp = puzzle.get(i, col)
            puzzle.set(i, col, puzzle.get(j, col))
            puzzle.set(j, col, temp)

        i += 1
        j -= 1

def __flip(puzzle: RegularSudoku) -> NoReturn:
    if 0 == randint(0, 2):
        __horizontal_flip(puzzle)
    if 0 == randint(0, 2):
        __vertical_flip(puzzle)

def __flip_box_by_row(puzzle: RegularSudoku, rowBoxes: int) -> NoReturn:
    row1 = randint(0, rowBoxes)
    row2 = randint(0, rowBoxes)

    if row1 != row2:
        distance = puzzle.box_rows * (max(row1, row2) - min(row1, row2))

        for i in range(puzzle.length):
            for j in range(puzzle.box_rows):
                temp = puzzle.get(i, j)
                puzzle.set(i, j, puzzle.get(i + distance, j))
                puzzle.set(i + distance, j, temp)

def __flip_box_by_col(puzzle: RegularSudoku, colBoxes: int) -> NoReturn:
    col1 = randint(0, colBoxes)
    col2 = randint(0, colBoxes)

    if col1 != col2:
        distance = puzzle.box_rows * abs(col1 - col2)

        for i in range(puzzle.length):
            for j in range(puzzle.box_rows):
                temp = puzzle.get(i, j)
                puzzle.set(i, j, puzzle.get(i, j + distance))
                puzzle.set(i, j + distance, temp)

def __flip_box(puzzle: RegularSudoku) -> NoReturn:
    rowBoxes = puzzle.row_boxes
    colBoxes = puzzle.col_boxes

    for _ in range(rowBoxes):
        __flip_box_by_row(puzzle, rowBoxes)
    for _ in range(colBoxes):
        __flip_box_by_col(puzzle, colBoxes)

def __swap_box_dimensions(puzzle: RegularSudoku) -> NoReturn:
    dimensionInfo = puzzle._info.dimensions.value

    temp = dimensionInfo["boxRows"]
    dimensionInfo["boxRows"] = dimensionInfo["boxCols"]
    dimensionInfo["boxCols"] = temp

def __inner_row(puzzle: RegularSudoku) -> NoReturn:
    boxRows = puzzle.box_rows
    rowIndex = 0
    rowEndIndex = puzzle.box_rows
    length = puzzle.length

    while rowEndIndex != length:
        rowToShuffle = randint(rowIndex, rowEndIndex)

        if rowToShuffle != rowIndex:
            for colIndex in range(length):
                temp = puzzle.get(rowIndex, colIndex)
                puzzle.set(rowIndex, colIndex, puzzle.get(rowToShuffle, colIndex))
                puzzle.set(rowToShuffle, colIndex, temp)

        rowIndex += 1
        if rowIndex == rowEndIndex:
            rowEndIndex += boxRows

def __inner_col(puzzle: RegularSudoku) -> NoReturn:
    boxCols = puzzle.box_cols
    colIndex = 0
    colEndIndex = puzzle.box_cols
    length = puzzle.length

    while colEndIndex != length:
        colToShuffle = randint(colIndex, colEndIndex)

        if colToShuffle != colIndex:
            for rowIndex in range(length):
                temp = puzzle.get(rowIndex, colIndex)
                puzzle.set(rowIndex, colIndex, puzzle.get(rowIndex, colToShuffle))
                puzzle.set(rowIndex, colToShuffle, temp)

        colIndex += 1
        if colIndex == colEndIndex:
            colEndIndex += boxCols

def __inner(puzzle: RegularSudoku) -> NoReturn:
    __inner_row(puzzle)
    __inner_col(puzzle)

def __rotate90(puzzle: RegularSudoku) -> NoReturn:
    for i in range(puzzle.length // 2):
        x = puzzle.length - 1 - i

        for j in range(i, x):
            y = puzzle.length - 1 - j

            temp = puzzle.get(i, j)
            puzzle.set(i, j, puzzle.get(j, x))
            puzzle.set(j, x, puzzle.get(x, y))
            puzzle.set(x, y, puzzle.get(y, i))
            puzzle.set(y, i, temp)

    __swap_box_dimensions(puzzle)

def __rotate180(puzzle: RegularSudoku) -> NoReturn:
    __rotate90(puzzle)
    __rotate90(puzzle)

def __rotate270(puzzle: RegularSudoku) -> NoReturn:
    for i in range(puzzle.length // 2):
        x = puzzle.length - 1 - i

        for j in range(i, x):
            y = puzzle.length - 1 - j

            temp = puzzle.get(i, j)
            puzzle.set(i, j, puzzle.get(y, i))
            puzzle.set(y, i, puzzle.get(x, y))
            puzzle.set(x, y, puzzle.get(j, x))
            puzzle.set(j, x, temp)

    __swap_box_dimensions(puzzle)

def __rotate(puzzle: RegularSudoku) -> NoReturn:
    choice = randint(0, 4)

    if 0 == choice:
        __rotate90(puzzle)
    elif 1 == choice:
        __rotate180(puzzle)
    elif 2 == choice:
        __rotate270(puzzle)

def __assign_swaps(puzzle: RegularSudoku, legalValues: List[str]) -> Dict[str, str]:
    shuffle(legalValues)

    legalCopy = puzzle.legal
    swapper = {}

    for (value1, value2) in zip(legalValues, legalCopy):
        swapper[value1] = value2

    return swapper

def __swap(puzzle: RegularSudoku, legalValues: List[str]) -> NoReturn:
    swapper = __assign_swaps(puzzle, legalValues)
    length = puzzle.length

    for rowIndex in range(length):
        for colIndex in range(length):
            value = puzzle.get(rowIndex, colIndex)

            if value is not None:
                puzzle.set(rowIndex, colIndex, swapper[value])

def _shuffle_board(puzzle: RegularSudoku, legalValues: List[str]) -> NoReturn:
    __flip(puzzle)
    __flip_box(puzzle)
    __inner(puzzle)
    __rotate(puzzle)
    __swap(puzzle, legalValues)
