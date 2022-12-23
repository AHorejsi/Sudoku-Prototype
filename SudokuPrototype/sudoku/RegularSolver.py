from typing import List, NoReturn, Any
from sudoku.RegularSudoku import RegularSudoku

def __index(rowIndex: int, colIndex: int, valueIndex: int, length: int) -> int:
    return rowIndex * length * length + colIndex * length + valueIndex

def __check_cell_constraint(hBase: int, matrix: List[List[bool]], length: int) -> int:
    for rowIndex in range(length):
        for colIndex in range(length):
            for valueIndex in range(length):
                index = __index(rowIndex, colIndex, valueIndex, length)
                matrix[index][hBase] = True

            hBase += 1

    return hBase

def __check_row_constraint(hBase: int, matrix: List[List[bool]], length: int) -> int:
    for rowIndex in range(length):
        for valueIndex in range(length):
            for colIndex in range(length):
                index = __index(rowIndex, colIndex, valueIndex, length)
                matrix[index][hBase] = True

            hBase += 1

    return hBase

def __check_col_constraint(hBase: int, matrix: List[List[bool]], length: int) -> int:
    for colIndex in range(length):
        for valueIndex in range(length):
            for rowIndex in range(length):
                index = __index(rowIndex, colIndex, valueIndex, length)
                matrix[index][hBase] = True

            hBase += 1

    return hBase

def __traverse_box(
        hBase: int,
        matrix: List[List[bool]],
        rowIndex: int,
        colIndex: int,
        valueIndex: int,
        length: int,
        boxRows: int,
        boxCols: int
) -> NoReturn:
    for rowDelta in range(boxRows):
        for colDelta in range(boxCols):
            index = __index(rowIndex + rowDelta, colIndex + colDelta, valueIndex, length)
            matrix[index][hBase] = True

def __check_box_constraint(hBase: int, matrix: List[List[bool]], length: int, boxRows: int, boxCols: int) -> NoReturn:
    for rowIndex in range(0, length, boxRows):
        for colIndex in range(0, length, boxCols):
            for valueIndex in range(length):
                __traverse_box(hBase, matrix, rowIndex, colIndex, valueIndex, length, boxRows, boxCols)

                hBase += 1

def __make_matrix(puzzle: RegularSudoku) -> List[List[bool]]:
    length = puzzle.length
    matrix = [[False] * (4 * length * length)] * (length * length * length)
    hBase = 0

    hBase = __check_cell_constraint(hBase, matrix, length)
    hBase = __check_row_constraint(hBase, matrix, length)
    hBase = __check_col_constraint(hBase, matrix, length)
    __check_box_constraint(hBase, matrix, length, puzzle.box_rows, puzzle.box_cols)

    return matrix

def __fill(values: list, fillValue: Any) -> NoReturn:
    for index in range(len(values)):
        values[index] = fillValue

def __place_initial_values(puzzle: RegularSudoku, matrix: List[List[bool]]) -> NoReturn:
    length = puzzle.length
    legalValues = puzzle.legal

    for rowIndex in range(length):
        for colIndex in range(length):
            value = puzzle.get(rowIndex, colIndex)

            if value is not None:
                for valueIndex in range(length):
                    if value != legalValues[valueIndex]:
                        index = __index(rowIndex, colIndex, valueIndex, length)
                        __fill(matrix[index], False)

def _has_unique_solution(puzzle: RegularSudoku) -> bool:
    legalValues = puzzle.legal
    answer = []

    matrix = __make_matrix(puzzle)
    __place_initial_values(puzzle, matrix)
