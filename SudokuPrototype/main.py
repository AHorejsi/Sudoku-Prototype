from sys import setrecursionlimit
from typing import NoReturn
from sudoku import generate_regular, RegularDimension, RegularDifficulty, RegularInfo

def __regular() -> NoReturn:
    puzzleList = []

    for dimension in RegularDimension:
        for difficulty in RegularDifficulty:
            info = RegularInfo(dimension, difficulty)
            new = generate_regular(info)

            puzzleList.append(new)

    for puzzle in puzzleList:
        print(puzzle)

def __hyper() -> NoReturn:
    pass

def __killer() -> NoReturn:
    pass

def __jigsaw() -> NoReturn:
    pass

if "__main__" == __name__:
    setrecursionlimit(10000)

    __regular()
    __hyper()
    __killer()
    __jigsaw()
