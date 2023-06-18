"""
 File containing all the option enums. These are used as types of constructor arguments in other classes.
"""

# Standard Library Imports
from enum import Enum



class DisplayUnit(Enum):
    """
     Enum used for unit which the results are displayed in. Passed as input argument to ecowcdb.Analysis class.

     Members:
         MicroSecond: Display the results in microseconds.
         MilliSecond: Display the results in milliseconds.
         Second: Display the results in seconds.
         Minute: Display the results in minutes.
         Hour: Display the results in hours.
    """
    MicroSecond = 0
    MilliSecond = 1
    Second = 2
    Minute = 3
    Hour = 4
    

class VerboseKW(Enum):
    """
     Enum used for verbosity keywords. Passed as input argument to ecowcdb.Analysis class.

     Members:
         Network: Prints the network during the construction of Analysis object.
         Forest: Prints each forest for which the delay is being computed.
         ES_ProgressBar: Displays a progressbar for exhaustive/partial search.
         FG_ProgressBar: Displays a progressbar for forest generation.
         LP_Details: Prints the names of lp files as they are being solved.
         LP_Errors: Prints the thrown LPError exceptions and their outcomes.
    """
    Network = 0
    Forest = 1
    ES_ProgressBar = 2
    FG_ProgressBar = 3
    LP_Details = 4
    LP_Errors = 5


class NetworkType(Enum):
    """
     Enum used for type of the network. Passed as input argument to ecowcdb.Networks class.

     Members:
         Symmetric: Network will be symmetric.
         AsymmetricFlow: First flow will have a higher arrival rate.
         AsymmetricServer: First server will have a lower service rate.
    """
    Symmetric = 0
    AsymmetricFlow = 1
    AsymmetricServer = 2


class ForestGeneration(Enum):
    """
     Enum used for forest generation mode. Passed as input argument to ecowcdb.Analysis class.

     Members:
         Empty: Do not generate any forests.
         Partial: Generate a subset of forests at random.
         All: Generate all valid forests.
    """
    Empty = 0
    Partial = 1
    All = 2
