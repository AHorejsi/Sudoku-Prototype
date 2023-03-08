from typing import List, Any
from sudoku.ExactCoverNode import _ExactCoverNode
from sudoku.StateError import StateError
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
):
    for rowDelta in range(boxRows):
        for colDelta in range(boxCols):
            index = __index(rowIndex + rowDelta, colIndex + colDelta, valueIndex, length)
            matrix[index][hBase] = True

def __check_box_constraint(hBase: int, matrix: List[List[bool]], length: int, boxRows: int, boxCols: int):
    for rowIndex in range(0, length, boxRows):
        for colIndex in range(0, length, boxCols):
            for valueIndex in range(length):
                __traverse_box(hBase, matrix, rowIndex, colIndex, valueIndex, length, boxRows, boxCols)

                hBase += 1

def __initialize_matrix(length: int) -> List[List[bool]]:
    matrix = []
    rowCount = length * length * length
    colCount = 4 * length * length

    for _ in range(rowCount):
        matrix.append([False] * colCount)

    return matrix

def __make_matrix(puzzle: RegularSudoku) -> List[List[bool]]:
    length = puzzle.length
    matrix = __initialize_matrix(length)
    hBase = 0

    hBase = __check_cell_constraint(hBase, matrix, length)
    hBase = __check_row_constraint(hBase, matrix, length)
    hBase = __check_col_constraint(hBase, matrix, length)
    __check_box_constraint(hBase, matrix, length, puzzle.box_rows, puzzle.box_cols)

    return matrix

def __fill(values: List[Any], fillValue: Any):
    for index in range(len(values)):
        values[index] = fillValue

def __place_value(value: str, rowIndex: int, colIndex: int, length: int, matrix: List[List[bool]], legalValues: str):
    for valueIndex in range(length):
        if value != legalValues[valueIndex]:
            index = __index(rowIndex, colIndex, valueIndex, length)
            __fill(matrix[index], False)

def __place_initial_values(puzzle: RegularSudoku, matrix: List[List[bool]]):
    length = puzzle.length
    legalValues = puzzle.legal

    for rowIndex in range(length):
        for colIndex in range(length):
            value = puzzle.get(rowIndex, colIndex)

            if value is not None:
                __place_value(value, rowIndex, colIndex, length, matrix, legalValues)

def __make_doubly_linked_matrix(matrix: List[List[bool]]) -> _ExactCoverNode:
    mainHead = _ExactCoverNode()
    headers = []
    cols = len(matrix[0])

    for _ in range(cols):
        headNode = _ExactCoverNode()

        headers.append(headNode)

        mainHead.hook_right(headNode)
        mainHead = headNode

    mainHead = mainHead.right.column

    for row in matrix:
        prev = None

        for col in range(cols):
            if row[col]:
                headNode = headers[col]
                newNode = _ExactCoverNode(headNode)

                if prev is None:
                    prev = newNode

                headNode.up.hook_down(newNode)
                prev.hook_right(newNode)

                prev = newNode

                headNode.size += 1

    mainHead.size = cols

    return mainHead

def __choose_next_column(header: _ExactCoverNode) -> _ExactCoverNode:
    minimum = None
    nextToUse = None
    colNode = header.right

    while colNode is not header:
        size = colNode.size

        if minimum is None or size < minimum:
            minimum = size
            nextToUse = colNode

        colNode = colNode.right

    return nextToUse


def __count_solutions(count: int, header: _ExactCoverNode) -> int:
    if header.right is header:
        count += 1
    else:
        colNode = __choose_next_column(header)
        colNode.cover()

        node1 = colNode.down

        while node1 is not colNode:
            node2 = node1.right

            while node2 is not node1:
                node2.column.cover()

                node2 = node2.right

            count = __count_solutions(count, header)

            if count > 1:
                return count

            colNode = node1.column

            node2 = node1.left

            while node2 is not node1:
                node2.column.uncover()

                node2 = node2.left

            node1 = node1.down

        colNode.uncover()

    return count

def _has_unique_solution(puzzle: RegularSudoku) -> bool:
    matrix = __make_matrix(puzzle)
    __place_initial_values(puzzle, matrix)
    header = __make_doubly_linked_matrix(matrix)

    solutionCount = __count_solutions(0, header)

    if 0 == solutionCount:
        raise StateError("No solutions found")
    else:
        return 1 == solutionCount
