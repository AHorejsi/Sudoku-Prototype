from typing import Optional
from final_class import final

@final
class StateError(RuntimeError):
    """
    Indicates that the associated object had one of its methods called
    while it was in a state that made the given operation invalid
    or impossible to perform
    """

    def __init__(self, message: Optional[str]=None):
        """
        Constructs a StateError with the specified message
        :param message: Detailed description of what caused the exception. Always a string
        """

        self.__message = message

    @property
    def message(self) -> Optional[str]:
        """
        Returns the message
        :return: The message associated with this StateError
        """

        return self.__message
