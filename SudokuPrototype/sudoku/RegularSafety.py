from typing import List, NoReturn
from BitVector import BitVector

class _RegularSafety:
    def __init__(self, length: int):
        bits = ~(~0 << length)

        self.__rowSafety: List[BitVector] = [BitVector(intVal=bits, size=length)] * length
        self.__colSafety: List[BitVector] = [BitVector(intVal=bits, size=length)] * length
        self.__boxSafety: List[BitVector] = [BitVector(intVal=bits, size=length)] * length

    @property
    def length(self) -> int:
        return len(self.__rowSafety)

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

    def solved(self) -> bool:
        return self.__solved(self.__rowSafety) and self.__solved(self.__colSafety) and self.__solved(self.__boxSafety)

    def __solved(self, safety: List[BitVector]) -> bool:
        for index in range(self.length):
            if 0 != safety[index].intValue:
                return False

        return True