from typing import List, Dict, Tuple
from random import shuffle
from copy import copy
from sudoku.StateError import StateError
from sudoku.RegularSudoku import RegularSudoku

def __next(puzzle: RegularSudoku, rowIndex: int, colIndex: int) -> (int, int):
    """
    Computes the row and column indices of the next position to be filled. Fills the entire, current row before moving
    to the next row. Shall only be called from within the ValueInitialization.py file
    :param puzzle: The sudoku board whose next open cell is to be searched for
    :param rowIndex: The row index to be used to determine the next position
    :param colIndex: The column index to be used to determine the next position
    :return: A tuple containing the next pair of row and column indices to be initialized with a value
    """

    length = puzzle.length

    while True:
        colIndex += 1

        if colIndex == length:
            rowIndex += 1
            colIndex = 0

        if rowIndex == length or puzzle.get(rowIndex, colIndex) is None:
            break

    return (rowIndex, colIndex)

def __initialize_values_helper2(
        puzzle: RegularSudoku,
        valueDict: Dict[Tuple[int, int], List[str]],
        prevRowIndex: int,
        prevColIndex: int
) -> bool:
    """
    Helper to perform the task of initializing the board with values
    :param puzzle: The sudoku board to be initialized with values
    :param valueDict: Dictionary containing shuffled lists to iterate through when attempting to assign a value
    :param prevRowIndex: The row index of the last cell to be assigned
    :param prevColIndex: The column index of the last cell to be assigned
    :return: True indicates that the puzzle has been completely filled, False otherwise
    :raises StateError: If the puzzle is not in a solved state by the end of the initialization
    """

    (rowIndex, colIndex) = __next(puzzle, prevRowIndex, prevColIndex)

    if puzzle.length == rowIndex:
        if not puzzle.is_solved():
            raise StateError(f"Sudoku board must be solved by this point\n{puzzle}")
        else:
            return True

    legalValues = valueDict[(rowIndex, colIndex)]


    for value in legalValues:
        if puzzle.is_safe(rowIndex, colIndex, value):
            puzzle.set(rowIndex, colIndex, value)

            if __initialize_values_helper2(puzzle, valueDict, rowIndex, colIndex):
                return True

            puzzle.delete(rowIndex, colIndex)

    return False

def __shuffle_values(legalValues: List[str], puzzle: RegularSudoku) -> Dict[Tuple[int, int], List[str]]:
    """
    For each pair of row and column indices in the board, a shuffled version of the initial list of legal values
    will be assigned. The result of each shuffling will be assigned to a corresponding row and column index pairs via
    a dictionary. The keys are a tuple containing the row and column indices and the values are the shuffled lists to
    be used for that position of the board. Shall only be called from within the ValueInitialization.py file
    :param legalValues: The values to copy and shuffle for each pair of row and column indices
    :return: A dictionary where the keys are the row and column indices and the values are the shuffled lists
    """

    length = len(legalValues)
    valueDict = {}

    for rowIndex in range(length):
        for colIndex in range(length):
            if puzzle.get(rowIndex, colIndex) is None:
                legalValuesCopy = copy(legalValues)
                shuffle(legalValuesCopy)

                valueDict[(rowIndex, colIndex)] = legalValuesCopy

    return valueDict


def __initialize_values_helper1(puzzle: RegularSudoku, legalValues: List[str]):
    """
    Initializes entire boxes of values that can be assigned independently of each other
    :param puzzle: The sudoku board to have its values initialized
    :param legalValues: The list of values that are allowed for this sudoku board
    :raises StateError: If the sudoku board is not valid by the end of this function
    """

    length = puzzle.length
    boxRows = puzzle.box_rows
    boxCols = puzzle.box_cols
    startRowIndex = 0
    startColIndex = 0
    values = copy(legalValues)

    while startRowIndex < length and startColIndex < length:
        index = 0

        shuffle(values)

        for rowIndex in range(startRowIndex, startRowIndex + boxRows):
            for colIndex in range(startColIndex, startColIndex + boxCols):
                puzzle.set(rowIndex, colIndex, values[index])

                index += 1

        startRowIndex += boxRows
        startColIndex += boxCols

    if not puzzle.is_valid():
        raise StateError(f"Sudoku board must be valid by this point\n{puzzle}")

def _initialize_values(puzzle: RegularSudoku, legalValues: List[str]):
    """
    Initializes an empty sudoku board with some values. The board shall be completely filled with a collection of
    values to make up a valid sudoku board. Shall only be called from within the sudoku package
    :param puzzle: The board to be initialized with values
    :param legalValues: A list of the allowed values for use in the board being initialized. Each value must be
        distinct, must be a string consisting of a single character, must have a length that is equal to the number of
        rows and columns in the sudoku board and must be in sorted order
    :raises StateError: If the sudoku board was not initialized properly and is not in a solved state by the end of
        initialization. This should never occur and, if it does, it means there is a problem with this function
    """

    __initialize_values_helper1(puzzle, legalValues)

    valueDict = __shuffle_values(legalValues, puzzle)

    __initialize_values_helper2(puzzle, valueDict, 0, 0)
