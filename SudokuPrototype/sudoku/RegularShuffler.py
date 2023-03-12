from math import sqrt
from random import randint, shuffle
from sudoku.RegularSudoku import RegularSudoku

def __horizontal_flip(puzzle: RegularSudoku):
    """
    Flips the sudoku board horizontally. Shall only be called from within RegularShuffler.py
    :param puzzle: The board to be flipped horizontally
    """

    i = 0
    j = puzzle.length - 1

    while i < j:
        for row in range(puzzle.length):
            temp = puzzle.get(row, i)
            puzzle.set(row, i, puzzle.get(row, j))
            puzzle.set(row, j, temp)

        i += 1
        j -= 1

def __vertical_flip(puzzle: RegularSudoku):
    """
    Flips the sudoku board vertically. Shall only be called from within RegularShuffler.py
    :param puzzle: The board to be flipped vertically
    """

    i = 0
    j = puzzle.length - 1

    while i < j:
        for col in range(puzzle.length):
            temp = puzzle.get(i, col)
            puzzle.set(i, col, puzzle.get(j, col))
            puzzle.set(j, col, temp)

        i += 1
        j -= 1

def __flip(puzzle: RegularSudoku):
    """
    Randomly flips vertically, horizontally, both or not at all.
    Shall only be called from within RegularShuffler.py
    :param puzzle: The sudoku board to be flipped
    """

    if 0 == randint(0, 2):
        __horizontal_flip(puzzle)
    if 0 == randint(0, 2):
        __vertical_flip(puzzle)

def __swap_row_boxes(puzzle: RegularSudoku, rowBoxIndex1: int, rowBoxIndex2: int):
    """
    Swaps the specified rows of boxes. Shall only be called from within RegularShuffler.py
    :param puzzle: The puzzle to have rows of boxes swapped
    :param rowBoxIndex1: The first index of the row of boxes to be swapped
    :param rowBoxIndex2: The second index of the row of boxes to be swapped
    """

    length = puzzle.length
    boxRows = puzzle.box_rows
    rowIndex1 = rowBoxIndex1 * boxRows
    rowIndex2 = rowBoxIndex2 * boxRows

    for _ in range(boxRows):
        for colIndex in range(length):
            temp = puzzle.get(rowIndex1, colIndex)
            puzzle.set(rowIndex1, colIndex, puzzle.get(rowIndex2, colIndex))
            puzzle.set(rowIndex2, colIndex, temp)

        rowIndex1 += 1
        rowIndex2 += 1

def __flip_box_by_row(puzzle: RegularSudoku):
    """
    Swaps rows of boxes randomly. Shall only be called from within the RegularShuffler.py
    :param puzzle: The sudoku board to rows of boxes swapped randomly
    """

    lastRowBoxIndex = puzzle.row_box_count - 1

    for rowBoxIndex in range(lastRowBoxIndex):
        randRowBoxIndex = randint(rowBoxIndex, lastRowBoxIndex)

        if rowBoxIndex != randRowBoxIndex:
            __swap_row_boxes(puzzle, rowBoxIndex, randRowBoxIndex)

def __swap_col_boxes(puzzle: RegularSudoku, colBoxIndex1: int, colBoxIndex2: int):
    """
    Swaps the specified columns of boxes. Shall only be called from within RegularShuffler.py
    :param puzzle: The puzzle to have columns of boxes swapped
    :param colBoxIndex1: The first index of the column of boxes to be swapped
    :param colBoxIndex2: The second index of the column of boxes to be swapped
    """

    length = puzzle.length
    boxCols = puzzle.box_cols
    colIndex1 = colBoxIndex1 * boxCols
    colIndex2 = colBoxIndex2 * boxCols

    for _ in range(boxCols):
        for rowIndex in range(length):
            temp = puzzle.get(rowIndex, colIndex1)
            puzzle.set(rowIndex, colIndex1, puzzle.get(rowIndex, colIndex2))
            puzzle.set(rowIndex, colIndex2, temp)

        colIndex1 += 1
        colIndex2 += 1

def __flip_box_by_col(puzzle: RegularSudoku):
    """
    Swaps columns of boxes randomly. Shall only be called from within the RegularShuffler.py
    :param puzzle: The sudoku board to columns of boxes swapped randomly
    """

    lastColBoxIndex = puzzle.col_box_count - 1

    for colBoxIndex in range(lastColBoxIndex):
        randColBoxIndex = randint(colBoxIndex, lastColBoxIndex)

        if colBoxIndex != randColBoxIndex:
            __swap_col_boxes(puzzle, colBoxIndex, randColBoxIndex)

def __flip_box(puzzle: RegularSudoku):
    """
    Swaps rows/columns of boxes randomly. Shall only be called from within RegularShuffler.py
    :param puzzle: The sudoku board to have rows/columns of boxes swapped randomly
    """

    __flip_box_by_row(puzzle)
    __flip_box_by_col(puzzle)

def __swap_rows(puzzle: RegularSudoku, rowIndex1: int, rowIndex2: int, length: int):
    """
    Swaps the values within the given rows
    :param puzzle: The sudoku board to have its rows swapped
    :param rowIndex1: The first row index to be swapped
    :param rowIndex2: The second row index to be swapped
    :param length: The number of rows in the sudoku board
    """

    for colIndex in range(length):
        temp = puzzle.get(rowIndex1, colIndex)
        puzzle.set(rowIndex1, colIndex, puzzle.get(rowIndex2, colIndex))
        puzzle.set(rowIndex2, colIndex, temp)

def __inner_by_row(puzzle: RegularSudoku):
    """
    Swaps rows of the sudoku board with rows that are within the same rows of boxes. Shall only be called from
    within the RegularShuffler.py file
    :param puzzle: The sudoku board to have its rows swapped around
    """

    boxRows = puzzle.box_rows
    length = puzzle.length

    for startIndex in range(0, length, boxRows):
        lastIndex = startIndex + boxRows - 1

        for shuffleIndex in range(startIndex, lastIndex - 1):
            randIndex = randint(shuffleIndex, lastIndex)

            if shuffleIndex != randIndex:
                __swap_rows(puzzle, shuffleIndex, randIndex, length)

def __swap_cols(puzzle: RegularSudoku, colIndex1: int, colIndex2: int, length: int):
    """
    Swaps the values within the given columns
    :param puzzle: The sudoku board to have its columns swapped
    :param colIndex1: The first column index to be swapped
    :param colIndex2: The second column index to be swapped
    :param length: The number of columns in the sudoku board
    """

    for rowIndex in range(length):
        temp = puzzle.get(rowIndex, colIndex1)
        puzzle.set(rowIndex, colIndex1, puzzle.get(rowIndex, colIndex2))
        puzzle.set(rowIndex, colIndex2, temp)

def __inner_by_col(puzzle: RegularSudoku):
    """
    Swaps columns of the sudoku board with columns that are within the same column of boxes. Shall only be called from
    within the RegularShuffler.py file
    :param puzzle: The sudoku board to have its columns swapped around
    """

    boxCols = puzzle.box_cols
    length = puzzle.length

    for startIndex in range(0, length, boxCols):
        lastIndex = startIndex + boxCols - 1

        for shuffleIndex in range(startIndex, lastIndex - 1):
            randIndex = randint(shuffleIndex, lastIndex)

            if shuffleIndex != randIndex:
                __swap_cols(puzzle, shuffleIndex, randIndex, length)

def __inner(puzzle: RegularSudoku):
    """
    Randomly swaps rows/columns of the sudoku board with row/columns that are within the same row/column of boxes. Shall
    only be called from within the RegularShuffle.py file
    :param puzzle: The sudoku board to have its rows/columns swapped around
    """

    __inner_by_row(puzzle)
    __inner_by_col(puzzle)

def __rotate90(puzzle: RegularSudoku):
    """
    Rotates the given sudoku board by 90 degrees. Shall only be applied to sudoku boards whose number of rows/columns
    is a perfect square. Shall only be called from within the RegularShuffler.py file
    :param puzzle: The sudoku board to be rotated 90 degrees
    """

    length = puzzle.length

    for i in range(length // 2):
        x = length - 1 - i

        for j in range(i, x):
            y = length - 1 - j

            temp = puzzle.get(i, j)
            puzzle.set(i, j, puzzle.get(j, x))
            puzzle.set(j, x, puzzle.get(x, y))
            puzzle.set(x, y, puzzle.get(y, i))
            puzzle.set(y, i, temp)

def __reverse_middle_row(puzzle: RegularSudoku, length: int):
    """
    Reverses the middlemost row of a sudoku board with an odd number of rows. Shall only be called from within the
    RegularShuffler.py file
    :param puzzle: The sudoku board to have its middlemost row reversed
    :param length: The number of rows in the sudoku board
    """

    middleRowIndex = length // 2
    lowColIndex = 0
    highColIndex = length - 1

    while lowColIndex < highColIndex:
        temp = puzzle.get(middleRowIndex, lowColIndex)
        puzzle.set(middleRowIndex, lowColIndex, puzzle.get(middleRowIndex, highColIndex))
        puzzle.set(middleRowIndex, highColIndex, temp)

        lowColIndex += 1
        highColIndex -= 1

def __rotate180(puzzle: RegularSudoku):
    """
    Rotates the given sudoku board by 180 degrees. Shall only be called from within the RegularShuffler.py file
    :param puzzle: The sudoku board to be rotated 180 degrees
    :return:
    """

    length = puzzle.length

    for i in range(length // 2):
        for j in range(length):
            x = length - i - 1
            y = length - j - 1

            temp = puzzle.get(i, j)
            puzzle.set(i, j, puzzle.get(x, y))
            puzzle.set(x, y, temp)

    if 1 == length % 2:
        __reverse_middle_row(puzzle, length)

def __rotate270(puzzle: RegularSudoku):
    """
    Rotates the given sudoku board by 270 degrees. Shall only be applied to sudoku boards whose number of rows/columns
    is a perfect square. Shall only be called from within the RegularShuffler.py file
    :param puzzle: The sudoku board to be rotated 270 degrees
    """

    length = puzzle.length

    for i in range(length // 2):
        x = length - 1 - i

        for j in range(i, x):
            y = length - 1 - j

            temp = puzzle.get(i, j)
            puzzle.set(i, j, puzzle.get(y, i))
            puzzle.set(y, i, puzzle.get(x, y))
            puzzle.set(x, y, puzzle.get(j, x))
            puzzle.set(j, x, temp)

def __is_perfect_square(value: int) -> bool:
    """
    Checks if the given integer is a perfect square. Shall only be called from within the RegularShuffler.py file
    :param value: The value to be checked
    :return: True if the given integer is a perfect square, False otherwise
    """

    return value == int(sqrt(value) + 0.5) ** 2

def __rotate(puzzle: RegularSudoku):
    """
    Randomly rotates the sudoku board by 90, 180, or 270 degrees. Shall only be called from within the
    RegularShuffler.py file
    :param puzzle: The sudoku board to be rotated
    """

    if __is_perfect_square(puzzle.length):
        choice = randint(0, 4)

        if 0 == choice:
            __rotate90(puzzle)
        elif 1 == choice:
            __rotate180(puzzle)
        elif 2 == choice:
            __rotate270(puzzle)
        else:
            return
    else:
        choice = randint(0, 2)

        if 0 == choice:
            __rotate180(puzzle)
        else:
            return

def _shuffle_board_regular(puzzle: RegularSudoku):
    """
    Shuffles the sudoku board in a way that keeps the sudoku board valid. Shall only be called from within
    the sudoku package
    :param puzzle: The sudoku board to shuffle
    """

    for _ in range(5):
        for shuffler in [__inner, __flip_box]:
            shuffler(puzzle)

    for shuffler in [__flip, __rotate]:
        shuffler(puzzle)
