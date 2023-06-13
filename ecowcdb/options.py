# Standard Library Imports
from enum import Enum



class DisplayUnit(Enum):
    MicroSecond = 0
    MilliSecond = 1
    Second = 2
    Minute = 3
    Hour = 4
    


class VerboseKW(Enum):
    Network = 0
    Forest = 1
    ProgressBar = 2
    LPProgress = 3
    LPErrorMsg = 4



class NetworkType(Enum):
    Symmetric = 0
    AsymmetricFlow = 1
    AsymmetricServer = 2



class ForestGeneration(Enum):
    Empty = 0
    Partial = 1
    All = 2



