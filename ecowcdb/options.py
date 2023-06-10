# Standard Library Imports
from enum import Enum



class DisplayUnit(Enum):
    Second = 0
    MilliSecond = 1
    MicroSecond = 2



class VerboseKW(Enum):
    Network = 0
    Forest = 1
    LPProgress = 2
    LPErrorMsg = 3



class NetworkType(Enum):
    Symmetric = 0
    AsymmetricFlow = 1
    AsymmetricServer = 2