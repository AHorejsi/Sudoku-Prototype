from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import List, NoReturn, Optional, Dict
from sudoku.Cell import _Cell

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

    FOUR: Dict[str, int | str] = { "length": 4, "boxRows": 2, "boxCols": 2, "legal": "1234" }
    """
    Info for 4x4 boards. See docstring of 'RegularDimension for more details
    """

    SIX: Dict[str, int | str] = { "length": 6, "boxRows": 2, "boxCols": 3, "legal": "123456" }
    """
    Info for 6x6 boards. See docstring of 'RegularDimension for more details
    """

    EIGHT: Dict[str, int | str] = { "length": 8, "boxRows": 4, "boxCols": 2, "legal": "01234567" }
    """
    Info for 8x8 boards. See docstring of 'RegularDimension for more details
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

    BEGINNER: Dict[str, int | str] = { "name": "Beginner", "lowerBoundOfGivens": 58, "upperBoundOfGivens": 68, "lowerBoundOfGivensPerUnit": 55 }
    """
    Info for beginner-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    EASY: Dict[str, int | str] = { "name": "Easy", "lowerBoundOfGivens": 44, "upperBoundOfGivens": 57, "lowerBoundOfGivensPerUnit": 44 }
    """
    Info for easy-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    MEDIUM: Dict[str, int | str] = { "name": "Medium", "lowerBoundOfGivens": 40, "upperBoundOfGivens": 43, "lowerBoundOfGivensPerUnit": 44 }
    """
    Info for medium-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    HARD: Dict[str, int | str] = { "name": "Hard", "lowerBoundOfGivens": 35, "upperBoundOfGivens": 38, "lowerBoundOfGivensPerUnit": 22 }
    """
    Info for hard-level puzzles. See docstring of 'RegularDifficulty for more info
    """

    MASTER: Dict[str, int | str] = { "name": "Master", "lowerBoundOfGivens": 21, "upperBoundOfGivens": 33, "lowerBoundOfGivensPerUnit": 0 }
    """
    Info for master-level puzzles. See docstring of 'RegularDifficulty for more info
    """

class RegularInfo:
    def __init__(self, dimensions: RegularDimension, difficulty: RegularDifficulty):
        self.__length = dimensions.value["length"]
        self.__boxRows = dimensions.value["boxRows"]
        self.__boxCols = dimensions.value["boxCols"]
        self.__legal = dimensions.value["legal"]
        self.__difficulty = difficulty.value["name"]
        self.__lowerBoundOfGivens = difficulty.value["lowerBoundOfGivens"]
        self.__upperBoundOfGivens = difficulty.value["upperBoundOfGivens"]
        self.__lowerBoundOfGivensPerUnit = difficulty.value["lowerBoundOfGivensPerUnit"]

    @property
    def length(self) -> int:
        return self.__length

    @property
    def box_rows(self)  -> int:
        return self.__boxRows

    @property
    def box_cols(self) -> int:
        return self.__boxCols

    @property
    def rows_in_boxes(self) -> int:
        return self.length // self.box_cols

    @property
    def cols_in_boxes(self) -> int:
        return self.length // self.box_rows

    def swap_box_dimensions(self) -> NoReturn:
        temp = self.__boxRows
        self.__boxRows = self.__boxCols
        self.__boxCols = temp

    @property
    def legal(self) -> str:
        return self.__legal

    @property
    def difficulty(self) -> str:
        return self.__difficulty

    @property
    def lower_bound_of_givens(self) -> int:
        return self.__lowerBoundOfGivens

    @property
    def upper_bound_of_givens(self) -> int:
        return self.__upperBoundOfGivens

    @property
    def lower_bound_of_givens_per_unit(self) -> int:
        return self.__lowerBoundOfGivensPerUnit


class _RegularSafety:
    def __init__(self, length: int):
        bits = ~(~0 << length)

        self.__length = length
        self.__rowSafety: List[int] = [bits] * length
        self.__colSafety: List[int] = [bits] * length
        self.__boxSafety: List[int] = [bits] * length

    def safe(self, rowIndex: int, colIndex: int, boxIndex: int, valueIndex: int) -> bool:
        mask = 1 << valueIndex

        rowSafe = 0 != self.__rowSafety[rowIndex] & mask
        colSafe = 0 != self.__colSafety[colIndex] & mask
        boxSafe = 0 != self.__boxSafety[boxIndex] & mask

        return rowSafe and colSafe and boxSafe

    def set_safe(self, rowIndex: int, colIndex: int, boxIndex: int, valueIndex: int) -> NoReturn:
        mask = 1 << valueIndex

        self.__rowSafety[rowIndex] |= mask
        self.__colSafety[colIndex] |= mask
        self.__boxSafety[boxIndex] |= mask

    def set_unsafe(self, rowIndex: int, colIndex: int, boxIndex: int, valueIndex: int) -> NoReturn:
        mask = ~(1 << valueIndex)

        self.__rowSafety[rowIndex] &= mask
        self.__colSafety[colIndex] &= mask
        self.__boxSafety[boxIndex] &= mask

    def __hamming_weight(self, val: int) -> int:
        val -= (val >> 1) & 0x5555555555555555
        val = (val & 0x3333333333333333) + ((val >> 2) & 0x3333333333333333)
        val = (val + (val >> 4)) & 0x0f0f0f0f0f0f0f0f
        val += val >> 8
        val += val >> 16
        val += val >> 32

        return val & 0x7f

    def weight(self, rowIndex: int, colIndex: int, boxIndex: int) -> (int, int, int):
        rowWeight = self.__hamming_weight(self.__rowSafety[rowIndex])
        colWeight = self.__hamming_weight(self.__colSafety[colIndex])
        boxWeight = self.__hamming_weight(self.__boxSafety[boxIndex])

        return (rowWeight, colWeight, boxWeight)

    def all_unsafe(self) -> bool:
        allRowsUnsafe = self.__all_unsafe_helper(self.__rowSafety)
        allColsUnsafe = self.__all_unsafe_helper(self.__colSafety)
        allBoxesUnsafe = self.__all_unsafe_helper(self.__boxSafety)

        return allRowsUnsafe and allColsUnsafe and allBoxesUnsafe

    def __all_unsafe_helper(self, safety: List[int]) -> bool:
        for index in range(self.__length):
            if 0 != safety[index]:
                return False

        return True

@dataclass
class RegularSudoku:
    __info: RegularInfo
    __table: List[_Cell]
    __safety: _RegularSafety

    @property
    def _info(self) -> RegularInfo:
        return self.__info

    def __order(self, value: str) -> int:
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
    def length(self) -> int:
        return self.__info.length

    @property
    def box_rows(self) -> int:
        return self.__info.box_rows

    @property
    def box_cols(self) -> int:
        return self.__info.box_cols

    @property
    def rows_in_boxes(self) -> int:
        return self.__info.rows_in_boxes

    @property
    def cols_in_boxes(self) -> int:
        return self.__info.cols_in_boxes

    def is_legal(self, value: str) -> bool:
        return value is None or -1 != self.__order(value)

    def is_safe(self, rowIndex: int, colIndex: int, value: str) -> bool:
        self.__check_bounds(rowIndex, colIndex)

        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        return self.__safety.safe(rowIndex, colIndex, boxIndex, valueIndex)

    def __set_unsafe(self, rowIndex: int, colIndex: int, value: str) -> NoReturn:
        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        self.__safety.set_unsafe(rowIndex, colIndex, boxIndex, valueIndex)

    def __set_safe(self, rowIndex: int, colIndex: int, value: str) -> NoReturn:
        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        self.__safety.set_safe(rowIndex, colIndex, boxIndex, valueIndex)

    def _weight(self, rowIndex: int, colIndex: int) -> (int, int, int):
        boxIndex = self.__box_index(rowIndex, colIndex)

        return self.__safety.weight(rowIndex, colIndex, boxIndex)

    def __get_cell(self, rowIndex: int, colIndex: int) -> _Cell:
        self.__check_bounds(rowIndex, colIndex)

        return self.__table[self.__actual_index(rowIndex, colIndex)]

    def __check_bounds(self, rowIndex: int, colIndex: int) -> NoReturn:
        length = self.length

        if rowIndex < 0 or rowIndex >= length or colIndex < 0 or colIndex >= length:
            raise IndexError(f"Indices out of bounds: [rowIndex: {rowIndex}, colIndex: {colIndex}, length: {length}]")

    def get(self, rowIndex: int, colIndex: int) -> Optional[str]:
        return self.__get_cell(rowIndex, colIndex).value

    def set(self, rowIndex: int, colIndex: int, newValue: Optional[str]) -> NoReturn:
        if not self.is_legal(newValue):
            raise ValueError("Invalid character")

        cell = self.__get_cell(rowIndex, colIndex)
        oldValue = cell.value

        if not oldValue is None:
            self.__set_safe(rowIndex, colIndex, oldValue)
        if not newValue is None:
            self.__set_unsafe(rowIndex, colIndex, newValue)

        cell.value = newValue

    def delete(self, rowIndex: int, colIndex: int) -> NoReturn:
        self.set(rowIndex, colIndex, None)

    def is_editable(self, rowIndex: int, colIndex: int) -> bool:
        return self.__get_cell(rowIndex, colIndex).editable

    def __actual_index(self, rowIndex: int, colIndex: int) -> int:
        return rowIndex * self.length + colIndex

    def __box_index(self, rowIndex: int, colIndex: int) -> int:
        return rowIndex // self.__info.box_rows * self.__info.box_rows + colIndex // self.__info.box_cols

    def _finalize(self) -> NoReturn:
        for cell in self.__table:
            if cell.value is not None:
                cell._make_noneditable()

    def is_solved(self) -> bool:
        return self.__safety.all_unsafe()

    def __repr__(self):
        length = self.length
        result = f"{self.__info.difficulty}\n"

        for (count, cell) in enumerate(self.__table, 1):
            result += "*" if cell.value is None else cell.value

            if 0 == count % length:
                result += "\n"

        return result
