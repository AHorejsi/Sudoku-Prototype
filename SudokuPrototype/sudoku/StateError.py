class StateError(RuntimeError):
    """
    Indicates that the associated object had one of its methods called
    while it was in a state that made the given operation invalid
    or impossible to perform
    """

    def __init__(self, message: str):
        """
        Constructs a StateError with the specified message
        :param message: Detailed description of what caused the exception. Always a string
        """

        self.__message = message

    @property
    def message(self) -> str:
        """
        Returns the message

        :return:
        """

        return self.__message
