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
    
    def error_type(self) -> LPErrorType:
        return self._error_type

def check_LP_error(s: str) -> None:
    s_split = s.split('\n')
    if s_split[-2] == 'Timeout':
        raise LPError(LPErrorType.TimeoutError)
    if s_split[-2] == 'Accuracy error':
        raise LPError(LPErrorType.AccuracyError)
    if s_split[0] == 'Suboptimal solution':
        raise LPError(LPErrorType.SuboptimalSolutionWarning)