"""
 File containing the custom error class and its utility functions. Used to catch and communicate lp_solve related
 errors.
"""

# Standard Library Imports
from enum import Enum



class LPErrorType(Enum):
    """
     Enum used for type of the error.

     Members:
         AccuracyError: lp_solve could not satisfy the constraints.
         TimeoutError: lp_solve could not solve within the given time limit.
         InfeasibleProblemError: lp is infeasible.
         UnboundedProblemError: lp is unbounded.
         LPSolveFailure: lp_solve failed.
         SuboptimalSolutionWarning: lp_solve did not reach optimal solution within the given time limit.
         UnhandledLPError: None of the defined errors were detected, but the output is not valid either.
    """
    AccuracyError = 0
    TimeoutError = 1
    InfeasibleProblemError = 2
    UnboundedProblemError = 3
    LPSolveFailure = 4
    SuboptimalSolutionWarning = 5
    UnhandledLPError = 6


class LPError(Exception):
    """
     Error class used to indicate types of errors related to lp_solve.

     Attributes:
         __error_type (LPErrorType, private): Type of the error.

     Methods:
         error_type (public): Gets the error_type of this LPError.

    """
    __error_type: LPErrorType

    def __init__(self, error_type: LPErrorType) -> None:
        """
         Initialize the LPError object. This is the constructor for the class.
         
         Args:
         	 error_type (LPErrorType, required): The type of error to be raised.
        """
        self.__error_type = error_type

    def __str__(self) -> str:
        """
         Returns a string representation of the LPError.
         
         Returns: 
         	 str: A string representation of the LPError.
        """
        return f'LPError: {self.__error_type.name}'
    
    def error_type(self) -> LPErrorType:
        """
         Gets the error_type of this LPError.
         
         Returns: 
         	 LPErrorType: The error_type of this LPError.
        """
        return self.__error_type


def check_LP_error(s: str) -> None:
    """
     Called after every lp_solve call. Raises exceptions if necessary.
     
     Args:
     	 s (str, required): The string to check. Output of lp_solve.
     
     Raises: 
     	 LPError: The correct type of LPError.
    """
    s_split = s.split('\n')
    
    # Known and handled errors:
    if s_split[-2] == 'Accuracy error':
        raise LPError(LPErrorType.AccuracyError)
    if s_split[-2] == 'Timeout':
        raise LPError(LPErrorType.TimeoutError)
    if s_split[0] == 'This problem is infeasible':
        raise LPError(LPErrorType.InfeasibleProblemError)
    if s_split[0] == 'This problem is unbounded':
        raise LPError(LPErrorType.UnboundedProblemError)
    if s_split[-2] == 'lp_solve failed':
        raise LPError(LPErrorType.LPSolveFailure)
    if s_split[0] == 'Suboptimal solution':
        raise LPError(LPErrorType.SuboptimalSolutionWarning)
    
    # General check for correctness of the output:
    if s_split[1].startswith('Value of objective function:'):
        return
    raise LPError(LPErrorType.UnhandledLPError)
    