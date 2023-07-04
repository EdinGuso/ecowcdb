"""
 File containing the ECOWCDB (Efficient Computation Of Worst-Case Delay-Bounds) class.
"""

# Standard Library Imports
from time import time
from typing import List, Tuple

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

# Local Imports - utility libraries
from ecowcdb.util.errors import LPError, LPErrorType
from ecowcdb.util.network import heuristic_algorithm, scale_network
from ecowcdb.util.validation import Validation



class ECOWCDB:
    """
     Class for computing best delays for networks. (Disclaimer: The functions provided in this class are heurtistic
     functions based on analytical observations and statistics. The functions may not provide the best possible or
     shortest runtime delays.)

     Attributes:
         __validation (Validation.ECOWCDB, private): Validation object used to validate user inputs.
         __net (Network, private): The network object for which the delay will be computed.
         __edges (List[Tuple[int, int]], private): Directed graph representation of the network.
         __temp_folder (str, private): Folderpath in which the .lp files will be stored in.

     Methods:
         __delay (private): Computes the delay of the flow of interest for a given forest.
         min_cut_forest (public): Computes the best ecowcdb delay of the flow of interest.
         min_cut_forest_with_restricted_depth (public): Computes the best ecowcdb delay of the flow of interest for the
         given max_depth.
         min_cut_tree_with_restricted_depth (public): Computes a quick delay of the flow of interest for the given max_depth.
    """
    __validation: Validation.ECOWCDB
    __net: Network
    __edges: List[Tuple[int, int]]
    __temp_folder: str
    
    def __init__(self, net: Network, temp_folder: str = '') -> None:
        """
         Initialize ecowcdb. This function will validate all the inputs and generate everything needed to start the
         delay computation.
         
         Args:
         	 net (Network, required): The network for which the delay will be computed. This network cannot be modified
             after ECOWCDB object creation.
         	 temp_folder (str, optional): Folder to store temporary .lp files. It is the user's responsibility to
             ensure that the provided folder exists. Default is '' which means that temp files will be stored in the
             directory from where the intial call was made.
        """
        self.__validation = Validation.ECOWCDB()
        self.__validation.constructor_arguments(net, temp_folder)
        self.__net = net
        self.__edges = list(net.edges.keys())
        self.__temp_folder = temp_folder

    def __delay(self, foi: int, forest: List[Tuple[int, int]]) -> float:
        """
         Computes the delay of the flow of interest for a given forest. This function encapsulates all the interactions
         with the panco library. This is a helper function for delay.
         
         Args:
         	 foi (int, required): Flow of interest.
         	 forest (List[Tuple[int, int]], required): List of edges representing the forest.
         
         Returns: 
         	 float: The delay [seconds] or float('inf') if the delay could not be computed.
        """
        scale_factor = 1.0
        timeout = 1000
        while True:
            net = scale_network(self.__net, scale_factor)
            PLP = FifoLP(net, list_edges=forest, sfa=True, tfa=True, timeout=timeout, temp_folder=self.__temp_folder)
            PLP.forest = PLP.forest.make_feed_forward()
            try:
                return PLP.delay(foi)
            except LPError as lperror:
                if lperror.error_type() in [LPErrorType.AccuracyError, LPErrorType.TimeoutError,
                                            LPErrorType.LPSolveFailure]:
                    if scale_factor < 10**-2:
                        return float('inf')
                    else:
                        scale_factor *= 0.1
                elif lperror.error_type() in [LPErrorType.SuboptimalSolutionWarning]:
                    if timeout > 10**6:
                        return float('inf')
                    else:
                        timeout *= 10
                elif lperror.error_type() in [LPErrorType.InfeasibleProblemError, LPErrorType.UnboundedProblemError,
                                              LPErrorType.UnhandledLPError]:
                    return float('inf')
                else:
                    raise ValueError(f'Unhandled error type: {lperror}.')
                
    def min_cut_forest(self, foi: int) -> Tuple[float, float]:
        """
         Computes the best ecowcdb delay of the flow of interest. (Disclaimer: The obtained delay is not necessarily
         the best delay for this network. It is likely a very good delay, and it will likely take longer time to
         compute.)
         
         Args:
         	 foi (int, required): Flow of interest.
         
         Returns: 
         	 Tuple[float, float]: The delay [seconds] or float('inf') if the delay could not be computed and the
             runtime [seconds].
        """
        self.__validation.foi(foi, self.__net.num_flows)

        start = time()
        forest = heuristic_algorithm(self.__edges, self.__net.num_servers, self.__net.flows[foi].path)
        delay = self.__delay(foi, forest)
        end = time()
        runtime = end - start
        return (delay, runtime)


    def min_cut_forest_with_restricted_depth(self, foi: int, max_depth: int) -> Tuple[float, float]:
        """
         Computes the best ecowcdb delay of the flow of interest for the given max_depth. The resulting forest can have
         multiple components which are not connected. (Disclaimer: The obtained delay is not necessarily the best delay
         for this network for this depth. It is likely a very good delay for this depth, and it will likely take a
         moderate amount of time to compute.)
         
         Args:
         	 foi (int, required): Flow of interest.
         	 max_depth (int, optional): Maximum allowed depth of the forest. Negative values correspond to unlimited
             depth (same as best_delay). If it is a non-negative value, flow preservation is not guaranteed and the
             best ecowcdb delay may not be obtained.
         
         Returns:
         	 Tuple[float, float]: The delay [seconds] or float('inf') if the delay could not be computed and the
             runtime [seconds].
        """
        self.__validation.foi(foi, self.__net.num_flows)
        self.__validation.max_depth(max_depth)

        start = time()
        forest = heuristic_algorithm(self.__edges, self.__net.num_servers, self.__net.flows[foi].path, max_depth)
        delay = self.__delay(foi, forest)
        end = time()
        runtime = end - start
        return (delay, runtime)
    
    def min_cut_tree_with_restricted_depth(self, foi: int, max_depth: int) -> Tuple[float, float]:
        """
         Computes a quick delay of the flow of interest for the given max_depth. The resulting forest has a single
         component. After an edge is cut, no further edges along that path are considered. (Disclaimer: The obtained
         delay is not necessarily the quickest delay for this network for this depth. It is likely a mediocre delay
         for this depth, and it will likely take shorter time to compute.)
         
         Args:
         	 foi (int, required): Flow of interest.
         	 max_depth (int, optional): Maximum allowed depth of the forest. Negative values correspond to unlimited
             depth (same as best_delay). If it is a non-negative value, flow preservation is not guaranteed and the
             best ecowcdb delay may not be obtained.
         
         Returns: 
         	 Tuple[float, float]: The delay [seconds] or float('inf') if the delay could not be computed and the
             runtime [seconds].
        """
        self.__validation.foi(foi, self.__net.num_flows)
        self.__validation.max_depth(max_depth)

        start = time()
        forest = heuristic_algorithm(self.__edges, self.__net.num_servers, self.__net.flows[foi].path, max_depth, True)
        delay = self.__delay(foi, forest)
        end = time()
        runtime = end - start
        return (delay, runtime)
