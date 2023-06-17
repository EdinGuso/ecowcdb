"""
 File containing all the option enums. These are used as types of constructor arguments in other classes.
"""

# Standard Library Imports
from enum import Enum



class DisplayUnit(Enum):
    """
     Enum used for unit which the results are displayed in.
    """
    MicroSecond = 0
    MilliSecond = 1
    Second = 2
    Minute = 3
    Hour = 4
    

class VerboseKW(Enum):
    """
     Enum used for verbosity keywords.
    """
    Network = 0
    Forest = 1
    ProgressBar = 2
    ForestProgressBar = 3
    LPProgress = 4
    LPErrorMsg = 5


class NetworkType(Enum):
    """
     Enum used for type of the network.
    """
    Symmetric = 0
    AsymmetricFlow = 1
    AsymmetricServer = 2


class ForestGeneration(Enum):
    """
     Enum used for forest generation mode.
    """
    Empty = 0
    Partial = 1
    All = 2
