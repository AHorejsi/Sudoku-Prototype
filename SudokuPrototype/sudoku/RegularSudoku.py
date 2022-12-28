from __future__ import annotations
from typing import List, NoReturn, Optional
from BitVector import BitVector
from sudoku.Cell import _Cell
from sudoku.SudokuInfo import SudokuInfo

class _RegularSafety:
    def __init__(self, length: int):
        bits = ~(~0 << length)

        self.__rowSafety: List[BitVector] = [BitVector(intVal=bits, size=length)] * length
        self.__colSafety: List[BitVector] = [BitVector(intVal=bits, size=length)] * length
        self.__boxSafety: List[BitVector] = [BitVector(intVal=bits, size=length)] * length

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

    def weight(self, rowIndex: int, colIndex: int, boxIndex: int) -> (int, int, int):
        rowWeight = self.__rowSafety[rowIndex].count_bits()
        colWeight = self.__colSafety[colIndex].count_bits()
        boxWeight = self.__boxSafety[boxIndex].count_bits()

        return (rowWeight, colWeight, boxWeight)

class RegularSudoku:
    def __init__(self, info: SudokuInfo, table: List[_Cell], safety: _RegularSafety):
        self.__info: SudokuInfo = info
        self.__table: List[_Cell] = table
        self.__safety: _RegularSafety = safety

    @property
    def _info(self) -> SudokuInfo:
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
    def row_boxes(self) -> int:
        return self.length // self.box_cols

    @property
    def col_boxes(self) -> int:
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
            raise IndexError("Indices out of bounds")

    def get(self, rowIndex: int, colIndex: int) -> Optional[str]:
        return self.__get_cell(rowIndex, colIndex).value

    def set(self, rowIndex: int, colIndex: int, newValue: Optional[str]) -> NoReturn:
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

    def solved(self) -> bool:
        # TODO
        pass

    def __repr__(self) -> str:
        length = self.length
        result = f"{self.difficulty}\n"

        for (count, cell) in enumerate(self.__table, 1):
            result += "*" if cell.value is None else cell.value

            if 0 == count % length:
                result += "\n"

        return result
