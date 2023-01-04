from dataclasses import dataclass
from typing import NoReturn, Optional
from sudoku import StateError

@dataclass
class _Cell:
    """
    Cell of a Sudoku board. Contains a value that may or may not be edited.
    A cell shall only be non-editable if it was part of the initial set of
    values of the Sudoku board
    """


    __value: Optional[str] = None
    """
    The value contained in this cell. Can be None to indicate that no value has been entered.
    Initially, set to None. Shall be treated as private
    """

    __editable: bool = True
    """
    Indicates that this cell can have its value edited. Used to prevent a Sudoku board's
    initial values from being changed. Initially, set to True and shall only be converted
    to False while generating Sudoku boards. Shall be treated as private
    """

    @property
    def value(self) -> Optional[str]:
        """
        Returns the value contained in this cell. Can be None to indicate that no value
        has been entered

        :return: The value contained in this cell or None if there isn't one
        """

        return self.__value

    @property
    def editable(self) -> bool:
        """
        Indicates whether this cell is editable. Used to prevent a Sudoku board's
        initial values from being changed

        :return: True if this cell is editable, False otherwise
        """

        return self.__editable

    @value.setter
    def value(self, value: Optional[str]) -> NoReturn:
        """
        Changes the value contained in this cell. Throws an exception
        if this cell is not editable

        :param value: the new value to place in this cell. Always None
            or a string consisting of one char
        :raises StateError: Caused if this cell is not editable
        """

        if not self.__editable:
            raise StateError("Non-editable cell")

        self.__value = value

    def _make_noneditable(self) -> NoReturn:
        """
        Converts this cell to a non-editable state. Shall only be called
        on cells that initially have values after generating a Sudoku board.
        Shall be treated as package-private
        """

        self.__editable = False
