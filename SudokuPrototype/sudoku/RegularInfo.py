from __future__ import annotations
from copy import copy
from typing import Dict
from enum import Enum

class Dimension(Enum):
    FOUR: Dict[str, int | str] = { "length": 4, "boxRows": 2, "boxCols": 2, "legal": "1234" }
    SIX: Dict[str, int | str] = { "length": 6, "boxRows": 2, "boxCols": 3, "legal": "123456" }
    EIGHT: Dict[str, int | str] = { "length": 8, "boxRows": 4, "boxCols": 2, "legal": "01234567" }
    NINE: Dict[str, int | str] = { "length": 9, "boxRows": 3, "boxCols": 3, "legal": "123456789" }
    TEN: Dict[str, int | str] = { "length": 10, "boxRows": 2, "boxCols": 5, "legal": "0123456789" }
    TWELVE: Dict[str, int | str] = { "length": 12, "boxRows": 3, "boxCols": 4, "legal": "0123456789AB" }
    FIFTEEN: Dict[str, int | str] = { "length": 15, "boxRows": 5, "boxCols": 3, "legal": "123456789ABCDEF" }
    SIXTEEN: Dict[str, int | str] = { "length": 16, "boxRows": 4, "boxCols": 4, "legal": "0123456789ABCDEF" }

class Difficulty(Enum):
    BEGINNER: Dict[str, int | str] = { "name": "Beginner", "lowerBoundOfGivens": 58, "upperBoundOfGivens": 68, "lowerBoundOfGivensPerUnit": 55 }
    EASY: Dict[str, int | str] = { "name": "Easy", "lowerBoundOfGivens": 44, "upperBoundOfGivens": 57, "lowerBoundOfGivensPerUnit": 44 }
    MEDIUM: Dict[str, int | str] = { "name": "Medium", "lowerBoundOfGivens": 40, "upperBoundOfGivens": 43, "lowerBoundOfGivensPerUnit": 44 }
    HARD: Dict[str, int | str] = { "name": "Hard", "lowerBoundOfGivens": 35, "upperBoundOfGivens": 38, "lowerBoundOfGivensPerUnit": 22 }
    MASTER: Dict[str, int | str] = { "name": "Master", "lowerBoundOfGivens": 21, "upperBoundOfGivens": 33, "lowerBoundOfGivensPerUnit": 0 }

class RegularInfo:
    def __init__(self, dimensions: Dimension, difficulty: Difficulty):
        self.__dimensions = copy(dimensions)
        self.__difficulty = copy(difficulty)

    @property
    def dimensions(self) -> Dimension:
        return self.__dimensions

    @property
    def difficulty(self) -> Difficulty:
        return self.__difficulty
