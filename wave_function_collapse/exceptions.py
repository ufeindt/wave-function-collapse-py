class WaveFunctionCollapseException(Exception):
    """Exception raised if there is an issue when collapsign the wave
    function.

    Attributes:
        message -- explanation of the issue.
    """

    def __init__(
        self,
        message,
    ):
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return self.message
