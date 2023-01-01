from __future__ import annotations
from copy import copy
from enum import Enum
from typing import List, NoReturn, Optional, Dict
from sudoku.Cell import _Cell

class RegularDimension(Enum):
    FOUR: Dict[str, int | str] = { "length": 4, "boxRows": 2, "boxCols": 2, "legal": "1234" }
    SIX: Dict[str, int | str] = { "length": 6, "boxRows": 2, "boxCols": 3, "legal": "123456" }
    EIGHT: Dict[str, int | str] = { "length": 8, "boxRows": 4, "boxCols": 2, "legal": "01234567" }
    NINE: Dict[str, int | str] = { "length": 9, "boxRows": 3, "boxCols": 3, "legal": "123456789" }
    TEN: Dict[str, int | str] = { "length": 10, "boxRows": 2, "boxCols": 5, "legal": "0123456789" }
    TWELVE: Dict[str, int | str] = { "length": 12, "boxRows": 3, "boxCols": 4, "legal": "0123456789AB" }
    FIFTEEN: Dict[str, int | str] = { "length": 15, "boxRows": 5, "boxCols": 3, "legal": "123456789ABCDEF" }
    SIXTEEN: Dict[str, int | str] = { "length": 16, "boxRows": 4, "boxCols": 4, "legal": "0123456789ABCDEF" }

class RegularDifficulty(Enum):
    BEGINNER: Dict[str, int | str] = { "name": "Beginner", "lowerBoundOfGivens": 58, "upperBoundOfGivens": 68, "lowerBoundOfGivensPerUnit": 55 }
    EASY: Dict[str, int | str] = { "name": "Easy", "lowerBoundOfGivens": 44, "upperBoundOfGivens": 57, "lowerBoundOfGivensPerUnit": 44 }
    MEDIUM: Dict[str, int | str] = { "name": "Medium", "lowerBoundOfGivens": 40, "upperBoundOfGivens": 43, "lowerBoundOfGivensPerUnit": 44 }
    HARD: Dict[str, int | str] = { "name": "Hard", "lowerBoundOfGivens": 35, "upperBoundOfGivens": 38, "lowerBoundOfGivensPerUnit": 22 }
    MASTER: Dict[str, int | str] = { "name": "Master", "lowerBoundOfGivens": 21, "upperBoundOfGivens": 33, "lowerBoundOfGivensPerUnit": 0 }

class RegularInfo:
    def __init__(self, dimensions: RegularDimension, difficulty: RegularDifficulty):
        self.__dimensions = copy(dimensions)
        self.__difficulty = copy(difficulty)

    @property
    def dimensions(self) -> RegularDimension:
        return self.__dimensions

    @property
    def difficulty(self) -> RegularDifficulty:
        return self.__difficulty

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
        oneZeroOneOne = 0x5555555555555555
        twoZeroesTwoOnes = 0x3333333333333333
        fourZeroesFourOnes = 0x0f0f0f0f0f0f0f0f

        val -= (val >> 1) & oneZeroOneOne
        val = (val & twoZeroesTwoOnes) + ((val >> 2) & twoZeroesTwoOnes)
        val = (val + (val >> 4)) & fourZeroesFourOnes
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

class RegularSudoku:
    def __init__(self, info: RegularInfo, table: List[_Cell], safety: _RegularSafety):
        self.__info: RegularInfo = info
        self.__table: List[_Cell] = table
        self.__safety: _RegularSafety = safety

    @property
    def _info(self) -> RegularInfo:
        return self.__info

    @property
    def length(self) -> int:
        return self.__info.dimensions.value["length"]

    @property
    def box_rows(self) -> int:
        return self.__info.dimensions.value["boxRows"]

    @property
    def box_cols(self) -> int:
        return self.__info.dimensions.value["boxCols"]

    @property
    def rows_in_box(self) -> int:
        return self.length // self.box_cols

    @property
    def cols_in_boxes(self) -> int:
        return self.length // self.box_rows

    @property
    def legal(self) -> str:
        return self.__info.dimensions.value["legal"]

    def __order(self, value: str) -> int:
        legalValues = self.legal
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

    def is_legal(self, value: str) -> bool:
        return -1 != self.__order(value)

    @property
    def difficulty(self) -> str:
        return self.__info.difficulty.value["name"]

    @property
    def lower_bound_of_givens(self) -> int:
        return self.__info.difficulty.value["lowerBoundOfGivens"]

    @property
    def upper_bound_of_givens(self) -> int:
        return self.__info.difficulty.value["upperBoundOfGivens"]

    @property
    def lower_bound_of_givens_per_unit(self) -> int:
        return self.__info.difficulty.value["lowerBoundOfGivensPerUnit"]

    def is_safe(self, rowIndex: int, colIndex: int, value: str) -> bool:
        self.__check_bounds(rowIndex, colIndex)

        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        return self.__safety.safe(rowIndex, colIndex, boxIndex, valueIndex)

    def __set_unsafe(self, rowIndex: int, colIndex: int, value: str) -> NoReturn:
        valueIndex = self.__order(value)
        boxIndex = self.__box_index(rowIndex, colIndex)

        self.__safety.set_unsafe(rowIndex, colIndex, boxIndex, valueIndex)

    def __set_safe(self, rowIndex: int, colIndex: int) -> NoReturn:
        value = self.get(rowIndex, colIndex)

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
        if newValue is not None and not self.is_legal(newValue):
            raise ValueError("Invalid character")

        cell = self.__get_cell(rowIndex, colIndex)

        if not cell.value is None:
            self.__set_safe(rowIndex, colIndex)
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
        return rowIndex // self.box_rows * self.box_rows + colIndex // self.box_cols

    def _finalize(self) -> NoReturn:
        for cell in self.__table:
            if cell.value is not None:
                cell._set_editable(False)

    def is_solved(self) -> bool:
        return self.__safety.all_unsafe()

    def __repr__(self):
        length = self.length
        result = f"{self.difficulty}\n"

        for (count, cell) in enumerate(self.__table, 1):
            result += "*" if cell.value is None else cell.value

            if 0 == count % length:
                result += "\n"

        return result
