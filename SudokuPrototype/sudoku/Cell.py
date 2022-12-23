from __future__ import annotations
from dataclasses import dataclass
from typing import NoReturn, Optional
from sudoku import StateError

@dataclass
class _Cell:
    __value: Optional[str]
    __editable: bool

    @property
    def value(self) -> Optional[str]:
        return self.__value

    @property
    def editable(self) -> bool:
        return self.__editable

    @value.setter
    def value(self, value: Optional[str]) -> NoReturn:
        if not self.__editable:
            raise StateError("Not editable cell")

        self.__value = value

    def _set_editable(self, editable: bool) -> NoReturn:
        self.__editable = editable
