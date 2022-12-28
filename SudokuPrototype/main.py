from sudoku import *

if "__main__" == __name__:
    for dimension in Dimension:
        for difficulty in Difficulty:
            info = RegularInfo(dimension, difficulty)

            puzzle = generate_regular(info)
            print(puzzle)
