from sys import setrecursionlimit
from sudoku import generate_regular, RegularDimension, RegularDifficulty, RegularInfo

def __regular():
    for dimension in RegularDimension:
        for difficulty in RegularDifficulty:
            info = RegularInfo(dimension, difficulty)
            new = generate_regular(info)

            print(new)
            print(f"Valid: {new.is_valid()}")
            print(f"Complete: {new.is_complete()}")
            print(f"Solved: {new.is_solved()}")
            print("\n")

def __hyper():
    pass

def __killer():
    pass

def __jigsaw():
    pass

if "__main__" == __name__:
    setrecursionlimit(10000)

    __regular()
    __hyper()
    __killer()
    __jigsaw()
