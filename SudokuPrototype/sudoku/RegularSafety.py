from typing import List, NoReturn

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