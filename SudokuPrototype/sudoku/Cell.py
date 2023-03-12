from typing import Optional, Set
from final_class import final
from sudoku import StateError

@final
class _Cell:
    """
    Cell of a Sudoku board. Contains a value that may or may not be edited.
    A cell shall only be non-editable if it was part of the initial set of
    values of the Sudoku board. Shall only be used from within the sudoku package
    """

    def __init__(self):
        """
        Makes an editable cell with no value
        """

        self.__value = None
        """
        The value contained in this cell. Can be None to indicate that no value has been entered.
        Initially, set to None. Shall only be accessed from within the _Cell class
        """

        self.__editable = True
        """
        Indicates that this cell can have its value edited. Used to prevent a Sudoku board's
        initial values from being changed. Initially, set to True and shall only be converted
        to False while generating Sudoku boards. Shall only be accessed from within the _Cell class
        """

        self.__tentative: Set[str] = set()
        """
        List of tentative values that could be assigned to this cell. Specified by the player.
        Shall only be accessed from within _Cell class
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

    @property
    def tentative(self) -> Set[str]:
        """
        Returns the set of tentative values specified by the player
        :return: The set of tentative values specified by the player
        """

        return self.__tentative

    @value.setter
    def value(self, value: Optional[str]):
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

    @editable.setter
    def editable(self, editable: bool):
        """
        Converts this cell to a non-editable state. Shall only be called
        on cells that initially have values after generating a Sudoku board.
        Shall only be called from within the sudoku package
        :raises StateError: If the cell contains no value. Making a cell with no value non-editable will prevent the
            board from being completed
        """

        if self.__value is None:
            raise StateError("Cannot make a cell with no value non-editable")

        self.__editable = editable
