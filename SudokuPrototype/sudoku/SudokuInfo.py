from __future__ import annotations
from copy import deepcopy
from typing import Dict
from enum import Enum

class DimensionInfo(Enum):
    FOUR: Dict[str, int | str] = { "length": 4, "boxRows": 2, "boxCols": 2, "legal": "1234" }
    SIX: Dict[str, int | str] = { "length": 6, "boxRows": 2, "boxCols": 3, "legal": "123456" }
    EIGHT: Dict[str, int | str] = { "length": 8, "boxRows": 4, "boxCols": 2, "legal": "01234567" }
    NINE: Dict[str, int | str] = { "length": 9, "boxRows": 3, "boxCols": 3, "legal": "123456789" }
    TEN: Dict[str, int | str] = { "length": 10, "boxRows": 2, "boxCols": 5, "legal": "0123456789" }
    TWELVE: Dict[str, int | str] = { "length": 12, "boxRows": 3, "boxCols": 4, "legal": "0123456789AB" }
    FIFTEEN: Dict[str, int | str] = { "length": 15, "boxRows": 5, "boxCols": 3, "legal": "123456789ABCDEF" }
    SIXTEEN: Dict[str, int | str] = { "length": 16, "boxRows": 4, "boxCols": 4, "legal": "0123456789ABCDEF" }

class DifficultyInfo(Enum):
    BEGINNER: Dict[str, int | str] = { "name": "beginner", "lowerBoundOfGivens": 58, "upperBoundOfGivens": 68, "lowerBoundOfGivensPerUnit": 55 }
    EASY: Dict[str, int | str] = { "name": "easy", "lowerBoundOfGivens": 44, "upperBoundOfGivens": 57, "lowerBoundOfGivensPerUnit": 44 }
    MEDIUM: Dict[str, int | str] = { "name": "medium", "lowerBoundOfGivens": 40, "upperBoundOfGivens": 43, "lowerBoundOfGivensPerUnit": 44 }
    HARD: Dict[str, int | str] = { "name": "hard", "lowerBoundOfGivens": 35, "upperBoundOfGivens": 38, "lowerBoundOfGivensPerUnit": 22 }
    MASTER: Dict[str, int | str] = { "name": "master", "lowerBoundOfGivens": 21, "upperBoundOfGivens": 33, "lowerBoundOfGivensPerUnit": 0 }

class SudokuInfo:
    def __init__(self, dimensions: DimensionInfo, difficulty: DifficultyInfo):
        self.__dimensions = deepcopy(dimensions)
        self.__difficulty = deepcopy(difficulty)

    @property
    def dimensions(self) -> DimensionInfo:
        return self.__dimensions

    @property
    def difficulty(self) -> DifficultyInfo:
        return self.__difficulty
