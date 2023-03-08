from __future__ import annotations
from dataclasses import dataclass
from final_class import final
from enum import Enum
from typing import List, Optional, Set, Dict, Tuple
from sudoku.Cell import _Cell

@final
class RegularDimension(Enum):
    """
    Specifies the dimensions allowed for regular sudoku boards.
    Each value has a corresponding dictionary specifying various properties
    for boards of the given number of dimensions. The properties contained
    in each dictionary are 'length', 'boxRows', 'boxCols' and 'legal'.
    'length' specifies the total number of rows and columns for a board.
    'boxRows' specifies the number of rows in each box.
    'boxCols' specifies the number of columns in each box.
    'legal' specifies the valid characters for the board, in sorted order
    """

    NINE: Dict[str, int | str] = { "length": 9, "boxRows": 3, "boxCols": 3, "legal": "123456789" }
    """
    Info for 9x9 boards. See docstring of 'RegularDimension for more details
    """

    TEN: Dict[str, int | str] = { "length": 10, "boxRows": 2, "boxCols": 5, "legal": "0123456789" }
    """
    Info for 10x10 boards. See docstring of 'RegularDimension for more details
    """

    TWELVE: Dict[str, int | str] = { "length": 12, "boxRows": 3, "boxCols": 4, "legal": "0123456789AB" }
    """
    Info for 12x12 boards. See docstring of 'RegularDimension for more details
    """

    FIFTEEN: Dict[str, int | str] = { "length": 15, "boxRows": 5, "boxCols": 3, "legal": "123456789ABCDEF" }
    """
    Info for 15x15 boards. See docstring of 'RegularDimension for more details
    """

    SIXTEEN: Dict[str, int | str] = { "length": 16, "boxRows": 4, "boxCols": 4, "legal": "0123456789ABCDEF" }
    """
    Info for 16x26 boards. See docstring of 'RegularDimension for more details
    """

    EIGHTEEN: Dict[str, int | str] = { "length": 18, "boxRows": 3, "boxCols": 6, "legal": "0123456789ABCDEFGH" }

    TWENTY: Dict[str, int | str] = { "length": 20, "boxRows": 4, "boxCols": 5, "legal": "0123456789ABCDEFGHIJ" }

@final
class RegularDifficulty(Enum):
    """
    Specifies the difficulty levels for regular sudoku boards.
    Each value has a dictionary specifying various properties that any generated board
    must meet. The properties contained in each dictionary are 'name', 'lowerBoundOfGivens', 'upperBoundOfGivens',
    'lowerBoundOfGivensPerUnit'. 'name' provides a string representation of the difficulty's name.
    'lowerBoundOfGivens' specifies the minimum percentage of initial values to be provided.
    'upperBoundOfGivens' specifies the maximum percentage of initial values to be provided.
    'lowerBoundOfGivensPerUnit' specifies the minimum percentage of initial values to be provided in all units.
    A unit refers to a given cells row, column and box
    """

    BEGINNER: Dict[str, int | str] = { "title": "Beginner", "initialLowerBoundOfGivens": 58, "initialUpperBoundOfGivens": 68, "initialLowerBoundOfGivensPerUnit": 55 }
    """
    Info for beginner-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    EASY: Dict[str, int | str] = { "title": "Easy", "initialLowerBoundOfGivens": 44, "initialUpperBoundOfGivens": 57, "initialLowerBoundOfGivensPerUnit": 44 }
    """
    Info for easy-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    MEDIUM: Dict[str, int | str] = { "title": "Medium", "initialLowerBoundOfGivens": 40, "initialUpperBoundOfGivens": 43, "initialLowerBoundOfGivensPerUnit": 44 }
    """
    Info for medium-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    HARD: Dict[str, int | str] = { "title": "Hard", "initialLowerBoundOfGivens": 35, "initialUpperBoundOfGivens": 38, "initialLowerBoundOfGivensPerUnit": 22 }
    """
    Info for hard-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    MASTER: Dict[str, int | str] = { "title": "Master", "initialLowerBoundOfGivens": 21, "initialUpperBoundOfGivens": 33, "initialLowerBoundOfGivensPerUnit": 0 }
    """
    Info for master-level puzzles. See docstring of 'RegularDifficulty for more info
    """

@final
class RegularInfo:
    """
    Serves as a container for the difficulty and dimension settings that
    will be used to construct and initialize a regular sudoku board
    """

    def __init__(self, dimensions: RegularDimension, difficulty: RegularDifficulty):
        """
        Stores the values contained in the dictionaries of both the dimension and
        difficulty settings
        :param dimensions: The dimension settings to use
        :param difficulty: The difficulty settings to use
        """

        dimensionsDict = dimensions.value
        difficultyDict = difficulty.value

        self.__length = dimensionsDict["length"]
        self.__boxRows = dimensionsDict["boxRows"]
        self.__boxCols = dimensionsDict["boxCols"]
        self.__legal = dimensionsDict["legal"]
        self.__difficulty = difficultyDict["title"]
        self.__initialLowerBoundOfGivens = difficultyDict["initialLowerBoundOfGivens"]
        self.__initialUpperBoundOfGivens = difficultyDict["initialUpperBoundOfGivens"]
        self.__initialLowerBoundOfGivensPerUnit = difficultyDict["initialLowerBoundOfGivensPerUnit"]

    @property
    def length(self) -> int:
        """
        Returns the number of rows and columns to use for the sudoku board
        :return: The number of rows and columns to use for the sudoku board
        """

        return self.__length

    @property
    def box_rows(self) -> int:
        """
        Returns the number of rows in each box of the sudoku board
        :return: The number of rows in each box of the sudoku board
        """

        return self.__boxRows

    @property
    def box_cols(self) -> int:
        """
        Returns the number of columns in each box of the sudoku board
        :return: The number of columns in each box of the sudoku board
        """

        return self.__boxCols

    @property
    def box_count_rowwise(self) -> int:
        """
        Returns the number of boxes from top to bottom
        :return: The number of boxes from top to bottom
        """

        return self.length // self.box_cols

    @property
    def box_count_colwise(self) -> int:
        """
        Returns the number of boxes from left to right
        :return: The number of boxes from left to right
        """

        return self.length // self.box_rows

    @property
    def legal(self) -> str:
        """
        Returns a string that contains all characters allowed to be entered into a
        given sudoku board. Is in sorted order
        :return: A string that contains all characters allowed to be entered into a
            given sudoku board. Is in sorted order
        """

        return self.__legal

    @property
    def difficulty(self) -> str:
        """
        Returns the name of the difficulty as a string
        :return: The name of the difficulty as a string
        """

        return self.__difficulty

    @property
    def initial_lower_bound_of_givens(self) -> int:
        """
        Returns the minimum percentage of initial values to supplied in the sudoku board
        :return: The minimum percentage of initial values to supplied in the sudoku board
        """

        return self.__initialLowerBoundOfGivens

    @property
    def initial_upper_bound_of_givens(self) -> int:
        """
        Returns the maximum percentage of initial values to supplied in the sudoku board
        :return: The maximum percentage of initial values to supplied in the sudoku board
        """

        return self.__initialUpperBoundOfGivens

    @property
    def initial_lower_bound_of_givens_per_unit(self) -> int:
        """
        Returns  the minimum percentage of initial values to be provided in all units.
        A unit refers to a given cells row, column and box
        :return: The minimum percentage of initial values to be provided in all units
        """

        return self.__initialLowerBoundOfGivensPerUnit

@final
class _RegularSafety:
    """
    Describes which parts of a corresponding sudoku board are safe for which values for each
    row, column and box
    """

    def __init__(self, length: int):
        """
        Creates a collection of bit vectors that track the safety of values for each row, column and box
        :param length: The number of rows and columns in the corresponding sudoku board
        """

        bits = ~(~0 << length)

        self.__length = length
        self.__rowSafety: List[int] = [bits] * length
        self.__colSafety: List[int] = [bits] * length
        self.__boxSafety: List[int] = [bits] * length

    def safe(self, rowIndex: int, colIndex: int, boxIndex: int, valueIndex: int) -> bool:
        """
        Checks if the given value is safe to be placed at the given row, column and box indices
        :param rowIndex: The row index to place the value
        :param colIndex: The column index to place the value
        :param boxIndex: The box index to place the value
        :param valueIndex: The bit index of the value to be placed
        :return: True if the given value can be placed at the given indices, False otherwise
        :raises IndexError: If any of the supplied indices are outside the bounds of the safety table
        """

        self.__check_bounds([rowIndex, colIndex, boxIndex, valueIndex])

        mask = 1 << valueIndex

        rowSafe = 0 != self.__rowSafety[rowIndex] & mask
        colSafe = 0 != self.__colSafety[colIndex] & mask
        boxSafe = 0 != self.__boxSafety[boxIndex] & mask

        return rowSafe and colSafe and boxSafe

    def set_safe(self, rowIndex: int, colIndex: int, boxIndex: int, valueIndex: int):
        """
        Marks the given row, column and box as safe for the given value
        :param rowIndex: The row index to be marked as safe for the given value
        :param colIndex: The column index to be marked as safe for the given value
        :param boxIndex: The box index to be marked as safe for the given value
        :param valueIndex: The bit index of the value to be marked as safe at the given indices
        :raises IndexError: If any of the supplied indices are outside the bounds of the safety table
        """

        self.__check_bounds([rowIndex, colIndex, boxIndex, valueIndex])

        mask = 1 << valueIndex

        self.__rowSafety[rowIndex] |= mask
        self.__colSafety[colIndex] |= mask
        self.__boxSafety[boxIndex] |= mask

    def set_unsafe(self, rowIndex: int, colIndex: int, boxIndex: int, valueIndex: int):
        """
        Marks the given row, column and box as unsafe for the given value
        :param rowIndex: The row index to be marked as unsafe for the given value
        :param colIndex: The column index to be marked as unsafe for the given value
        :param boxIndex: The box index to be marked as unsafe for the given value
        :param valueIndex: The bit index of the value to be marked as unsafe at the given indices
        :raises IndexError: If any of the supplied indices are outside the bounds of the safety table
        """

        self.__check_bounds([rowIndex, colIndex, boxIndex, valueIndex])

        mask = ~(1 << valueIndex)

        self.__rowSafety[rowIndex] &= mask
        self.__colSafety[colIndex] &= mask
        self.__boxSafety[boxIndex] &= mask

    def weight(self, rowIndex: int, colIndex: int, boxIndex: int) -> (int, int, int):
        """
        Returns the hamming weight at each index
        :param rowIndex: The row index whose hamming weight is to be computed
        :param colIndex: The column index whose hamming weight is to be computed
        :param boxIndex: The box index whose hamming weight is to be computed
        :return: A tuple containing the hamming weight for each index
        """

        self.__check_bounds([rowIndex, colIndex, boxIndex])

        rowWeight = self.__hamming_weight(self.__rowSafety[rowIndex])
        colWeight = self.__hamming_weight(self.__colSafety[colIndex])
        boxWeight = self.__hamming_weight(self.__boxSafety[boxIndex])

        return (rowWeight, colWeight, boxWeight)

    def __check_bounds(self, indices: List[int]):
        """
        Checks if any of the supplied indices are outside the bounds of the safety table.
        If any are, an exception is raised. Shall only be called from within the RegularSafety class
        :param indices: The list of indices to be checked for whether they are outside the bounds
            of the safety table
        :raises IndexError: If any of the supplied indices are outside the bounds of the safety table
        """

        for index in indices:
            if index < 0 or index >= self.__length:
                raise IndexError("Safety index out of bounds")

    def __hamming_weight(self, val: int) -> int:
        """
        Computes the hamming weight of the given int value. Shall only be called from within the RegularSafety class
        :param val: The value whose hamming weight is to be computed
        :return: The hamming weight of the given int value
        """

        val -= (val >> 1) & 0x5555555555555555
        val = (val & 0x3333333333333333) + ((val >> 2) & 0x3333333333333333)
        val = (val + (val >> 4)) & 0x0f0f0f0f0f0f0f0f
        val += val >> 8
        val += val >> 16
        val += val >> 32

        return val & 0x7f

@final
@dataclass
class RegularSudoku:
    """
    Represents a sudoku board that operates on the normal rules of sudoku. No additional rules, except
    the board is not restricted to being 9x9
    """

    __info: RegularInfo
    """
    Various info describing the properties of this sudoku board. Also contains parameters used for generating
    this sudoku board
    """

    __table: List[_Cell]
    """
    Cells that contain all of the values entered into the board and which tracks which values may be changed
    """

    __safety: _RegularSafety
    """
    Describes which places on the board are safe for certain values
    """

    def __order(self, value: str) -> int:
        """
        Returns the sorted position as an index of the supplied value.
        The sorted position is based on the assumption that a sorted array
        of legal values with no duplicates is being used. Should only be called from
        within the RegularSudoku class
        :param value: The value whose sorted position is to be searched for or -1 if the supplied value is illegal
        :return: The index of the supplied value in a sorted array of legal values with no duplicates
        """

        legalValues = self.__info.legal
        lowIndex = 0
        highIndex = len(legalValues) - 1

        while lowIndex <= highIndex:
            midIndex = (lowIndex + highIndex) // 2
            midValue = legalValues[midIndex]

            if midValue < value:
                lowIndex = midIndex + 1
            elif midValue > value:
                highIndex = midIndex - 1
            else:
                return midIndex

        return -1

    @property
    def _info(self) -> RegularInfo:
        """
        Returns the info object describing the dimension and difficulty settings
        for this sudoku board
        :return: The info object describing the dimension and difficulty settings for this sudoku board
        """

        return self.__info

    @property
    def length(self) -> int:
        """
        Returns the number of rows and columns of this sudoku board.
        All sudoku boards are square
        :return: The number of rows and columns of this sudoku board
        """

        return self.__info.length

    @property
    def box_rows(self) -> int:
        """
        Returns the number of rows within each box of this sudoku board
        :return: The number of rows within each box of this sudoku board
        """

        return self.__info.box_rows

    @property
    def box_cols(self) -> int:
        """
        Returns the number of columns within each box of this sudoku board
        :return: The number of columns within each box of this sudoku board
        """

        return self.__info.box_cols

    @property
    def box_count_rowwise(self) -> int:
        """
        Returns the number of boxes from top to bottom
        :return: The number of boxes from top to bottom
        """

        return self.__info.box_count_rowwise

    @property
    def box_count_colwise(self) -> int:
        """
        Returns the number of boxes from left to right
        :return: The number of boxes from left to right
        """

        return self.__info.box_count_colwise

    @property
    def legal(self) -> str:
        """
        Returns a sorted string that contains the legal values for this sudoku board
        :return: A sorted string that contains the legal values for this sudoku board
        """

        return self.__info.legal

    @property
    def difficulty(self) -> str:
        """
        Returns the name of the difficulty used for this sudoku board as a string
        :return: The name of the difficulty used for this sudoku board as a string
        """

        return self.__info.difficulty

    @property
    def initial_lower_bound_of_givens(self) -> int:
        """
        Returns the minimum percentage of initial values to supplied in this sudoku board
        :return: The minimum percentage of initial values to supplied in this sudoku board
        """

        return self.__info.initial_lower_bound_of_givens

    @property
    def initial_upper_bound_of_givens(self) -> int:
        """
        Returns the maximum percentage of initial values to supplied in this sudoku board
        :return: The maximum percentage of initial values to supplied in this sudoku board
        """

        return self.__info.initial_upper_bound_of_givens

    @property
    def initial_lower_bound_of_givens_per_unit(self) -> int:
        """
        Returns  the minimum percentage of initial values to be provided in all units.
        A unit refers to a given cells row, column and box
        :return: The minimum percentage of initial values to be provided in all units
        """

        return self.__info.initial_lower_bound_of_givens_per_unit

    def is_legal(self, value: str) -> bool:
        """
        Checks if the given value is legal for this sudoku board. Note that None is considered legal
        :param value: The value to be checked for legality
        :return: True if the value is None or contained in the list of legal values, False otherwise
        """

        return value is None or -1 != self.__order(value)

    def is_safe(self, rowIndex: int, colIndex: int, value: str) -> bool:
        """
        Checks if the given value can be safely placed at the given indices without
        conflicting with any already placed values
        :param rowIndex: The row index of the cell to be checked for safety with the given value
        :param colIndex: The column index of the cell to be checked for safety with the given value
        :param value: The value to be checked for whether it can be placed at the given
            row anc column indices safely
        :return: True if the given value can be placed at the given row and column index, False otherwise
        :raises IndexError: If the row and column indices are outside the bounds of the board
        """

        self.__check_bounds(rowIndex, colIndex)

        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        return self.__safety.safe(rowIndex, colIndex, boxIndex, valueIndex)

    def __set_unsafe(self, rowIndex: int, colIndex: int, value: str):
        """
        Sets the row, column and box corresponding to the given row and column indices
        as unsafe for the given value. Shall only be called from within the RegularSudoku class
        :param rowIndex: The row index of the row, column and box to be marked as unsafe for the given value
        :param colIndex: The column index of the row, column and box to be marked as unsafe for the given value
        :param value: The value to be marked as unsafe in the given row, column and box
        """

        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        self.__safety.set_unsafe(rowIndex, colIndex, boxIndex, valueIndex)

    def __set_safe(self, rowIndex: int, colIndex: int, value: str):
        """
        Sets the row, column and box corresponding to the given row and column indices
        as safe for the given value. Shall only be called from within the RegularSudoku class
        :param rowIndex: The row index of the row, column and box to be marked as safe for the given value
        :param colIndex: The column index of the row, column and box to be marked as safe for the given value
        :param value: The value to be marked as safe in the given row, column and box
        """

        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        self.__safety.set_safe(rowIndex, colIndex, boxIndex, valueIndex)

    def _givens(self, rowIndex: int, colIndex: int) -> Tuple[int, int, int]:
        """
        Computes the number of givens in the unit that the provided row and column indices
        belongs to. Shall only be called from within the sudoku package
        :param rowIndex: The row index of the unit to have its givens counted
        :param colIndex: The column index of the unit to have its givens counted
        :return: The number of givens in the unit that the provided row and column indices belongs to
        """

        length = self.length
        boxIndex = self.__box_index(rowIndex, colIndex)
        (rowEmptyCount, colEmptyCount, boxEmptyCount) = self.__safety.weight(rowIndex, colIndex, boxIndex)

        return (length - rowEmptyCount, length - colEmptyCount, length - boxEmptyCount)

    def __get_cell(self, rowIndex: int, colIndex: int) -> _Cell:
        """
        Retrieves the cell at the given row and column indices. Shall only be called from within the
        RegularSudoku class
        :param rowIndex: The row index of the cell to retrieve
        :param colIndex: The column index of the cell to retrieve
        :return: The cell at the given row and column indices
        :raises IndexError: If the row and column indices are outside the bounds of the board
        """

        self.__check_bounds(rowIndex, colIndex)

        return self.__table[self.__actual_index(rowIndex, colIndex)]

    def __check_bounds(self, rowIndex: int, colIndex: int):
        """
        Checks if the given row and column indices are outside the bounds of the matrix. If so, an exception is
        raised. Shall only be called from within the RegularSudoku class
        :param rowIndex: The row index to be checked for whether it is inside the bounds of the board
        :param colIndex: The column index to be checked for whether it is inside the bounds of the board
        :raises IndexError: If the row and column indices are outside the bounds of the board
        """

        length = self.length

        if rowIndex < 0 or rowIndex >= length or colIndex < 0 or colIndex >= length:
            raise IndexError(f"Indices out of bounds: [rowIndex: {rowIndex}, colIndex: {colIndex}, length: {length}]")

    def get(self, rowIndex: int, colIndex: int) -> Optional[str]:
        """
        Returns the value at the given row and column indices. None is returned if no value has been entered
        :param rowIndex: The row index of the value to retrieve
        :param colIndex: The column index of the value to retrieve
        :return: The value at the given row and column indices. None if no value has been entered
        :raises IndexError: If the row and column indices are outside the bounds of the board
        """

        return self.__get_cell(rowIndex, colIndex).value

    def set(self, rowIndex: int, colIndex: int, newValue: Optional[str]):
        """
        Sets the value at the given row and column indices and erases the current value in the process.
        The new value that is provided may be set to None to erase the currently contained value
        :param rowIndex: The row index of the value to be changed
        :param colIndex: The column index of the value to be changed
        :param newValue: The new value to place at the given row and column indices. Can be None
        :raises ValueError: If the new value is not a legal value
        :raises IndexError: If the row and indices are outside the bounds of the board
        :raises StateError: If the cell at the given row and column indices is non-editable
        """

        cell = self.__get_cell(rowIndex, colIndex)

        oldValue = cell.value
        cell.value = newValue

        if oldValue is not None:
            self.__set_safe(rowIndex, colIndex, oldValue)
        if newValue is not None:
            self.__set_unsafe(rowIndex, colIndex, newValue)

    def delete(self, rowIndex: int, colIndex: int):
        """
        Erases the value from the cell at the given row and column indices
        :param rowIndex: The row index of the value to be erased
        :param colIndex: The column index of the value to be erased
        :raises IndexError: If the row and column indices are outside the bounds of the board
        :raises StateError: If the cell at the given row and column indices is non-editable
        """

        self.set(rowIndex, colIndex, None)

    def is_editable(self, rowIndex: int, colIndex: int) -> bool:
        """
        Checks if the value at the given row and column indices is editable
        :param rowIndex: The row index of the value to be checked
        :param colIndex: The column index of the value to be checked
        :return: True if the value at the given row and column indices can be edited, False otherwise
        :raises IndexError: If the row and column indices are outside the bounds of the board
        """

        return self.__get_cell(rowIndex, colIndex).editable

    def __actual_index(self, rowIndex: int, colIndex: int) -> int:
        """
        Maps the given row and column indices to a 1D list index. Shall only be called from within the
        RegularSudoku class
        :param rowIndex: The row index to be mapped
        :param colIndex: The column index to be mapped
        :return: The actual index of the 1D list that stores the cells, given the provided row and column indices
        """

        return rowIndex * self.length + colIndex

    def __box_index(self, rowIndex: int, colIndex: int) -> int:
        """
        Returns the index of the box that contains the given row and column indices. Shall only be called from within
        the RegularSudoku class
        :param rowIndex: The row index containing the box whose index will be returned
        :param colIndex: The column index containing the box whose index will be returned
        :return: The index of the box that contains the given row and column indices
        """

        return rowIndex // self.__info.box_rows * self.__info.box_rows + colIndex // self.__info.box_cols

    def _finalize(self):
        """
        Performs any final steps for finishing the construction of a regular sudoku board. Especially for steps
        that require access to private fields/functions. Shall only be called from within the sudoku package
        """

        for cell in self.__table:
            if cell.value is not None:
                cell.editable = False

    def is_complete(self) -> bool:
        """
        Checks if every value in the board is filled out and is a valid value. The current configuration
        need not be a correct solution for this to return True
        :return: True if every value in the board is filled and is a valid value, False otherwise
        """

        for cell in self.__table:
            if cell.value is None:
                return False

        return True

    def is_solved(self) -> bool:
        """
        Checks if this sudoku board has been successfully filled out
        :return: True if this sudoku board has been successfully filled out, False otherwise
        """

        return self.is_complete() and self.is_valid()

    def is_valid(self) -> bool:
        """
        Checks if the current state of the board has any conflicts between any filled cells
        :return: True if the current state is valid, False otherwise
        """

        length = self.length

        rowSeen = [0] * length
        colSeen = [0] * length
        boxSeen = [0] * length

        for rowIndex in range(length):
            for colIndex in range(length):
                boxIndex = self.__box_index(rowIndex, colIndex)
                value = self.get(rowIndex, colIndex)

                if value is not None:
                    valueIndex = self.__order(value)

                    if -1 == valueIndex:
                        return False

                    mask = 1 << valueIndex

                    if rowSeen[rowIndex] & mask:
                        return False
                    else:
                        rowSeen[rowIndex] |= mask

                    if colSeen[colIndex] & mask:
                        return False
                    else:
                        colSeen[colIndex] |= mask

                    if boxSeen[boxIndex] & mask:
                        return False
                    else:
                        boxSeen[boxIndex] |= mask

        return True

    def __str__(self):
        """
        Builds a string representation of this board's current state
        :return: A string representation of this board's current state
        """

        length = self.length
        boxRows = self.box_rows
        boxCols = self.box_cols

        result = f"{self.difficulty} {length}x{length}\n"

        border = ("-" * (length + self.box_count_rowwise + 1)) + "\n"

        for rowIndex in range(length):
            if 0 == rowIndex % boxRows:
                result += border

            for colIndex in range(length):
                if 0 == colIndex % boxCols:
                    result += "|"

                value = self.get(rowIndex, colIndex)

                result += "*" if value is None else value

            result += "|\n"

        result += border

        return result

    def __repr__(self):
        """
        Returns the same result as __str__
        :return: The same result as __str__
        """

        return str(self)
