# Standard Library Imports
from enum import Enum



class LPErrorType(Enum):
    TimeoutError = 1
    AccuracyError = 2
    SuboptimalSolutionWarning = 3

class LPError(Exception):
    def __init__(self, error_type: LPErrorType) -> None:
        if not isinstance(error_type, LPErrorType):
            raise ValueError("Invalid error type")
        self._error_type = error_type

    def __str__(self) -> str:
        return f'LPError: {self._error_type.name}'
