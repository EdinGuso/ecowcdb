"""
 desc.
"""

# Standard Library Imports
from typing import List, Tuple

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

# Local Imports - utility libraries
from ecowcdb.util.errors import LPError, LPErrorType
from ecowcdb.util.network import flow_preserving_min_depth_max_forest, scale_network
from ecowcdb.util.validation import Validation



class ECOWCDB:
    __validation: Validation.ECOWCDB
    __net: Network
    __edges: List[Tuple[int, int]]
    __temp_folder: str
    
    def __init__(self, net: Network, temp_folder: str = '') -> None:
        self.__validation = Validation.ECOWCDB()
        self.__validation.constructor_arguments(net, temp_folder)
        self.__net = net
        self.__edges = list(net.edges.keys())
        self.__temp_folder = temp_folder

    def __delay(self, foi: int, forest: List[Tuple[int, int]]) -> float:
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

    def delay(self, foi: int, max_depth: int = -1) -> float:
        self.__validation.foi(foi, self.__net.num_flows)
        self.__validation.max_depth(max_depth)
        
        forest = flow_preserving_min_depth_max_forest(self.__edges, self.__net.num_servers, self.__net.flows[foi].path, max_depth)
        return self.__delay(foi, forest)



    # def __next_forest(self, flow_edges: List[Tuple[int, int]], i: int) -> bool:
    #     # CAN I ASSUME THAT FLOWS DO NOT HAVE CYCLES??
    #     if i < len(self.__PATH_RATE):
    #         while len(self.__selected_edges) / len(flow_edges) < self.__PATH_RATE[i]:
    #             next_edge = flow_edges[len(self.__selected_edges)]
    #             self.__selected_edges += [next_edge]
    #             self.__remaining_edges.remove(next_edge)
    #     elif i < len(self.__PATH_RATE) + len(self.__OTHER_RATE):
    #         if len(self.__remaining_edges) == 0:
    #             return False
    #         edge_added = False
    #         while (len(self.__selected_edges) - len(flow_edges)) / (len(list(self.__net.edges.keys())) - len(flow_edges)) < self.__OTHER_RATE[i-len(self.__PATH_RATE)]:
    #             for edge in self.__remaining_edges:
    #                 if edge not in self.__selected_edges and edge[1] in [e[0] for e in self.__selected_edges]:
    #                     if is_forest(self.__net.decomposition(self.__selected_edges + [edge])[0]):
    #                         self.__selected_edges += [edge]
    #                         self.__remaining_edges.remove(edge)
    #                         edge_added = True
    #                         break
    #             if not edge_added or len(self.__remaining_edges) == 0:
    #                 return False
    #     else:
    #         print('ERROR: should never enter this condition')
    #         return False
    #     return True



    # def delay(self, foi: int, time_limit: int | float) -> float:
    #     def timeout_handler(signum, frame):
    #         raise TimeoutError("Function timed out.")
    #     cls = '\r' + ' '*50 + '\r'
        
    #     self.__remaining_edges = list(self.__net.edges.keys())
    #     self.__selected_edges = []

    #     best_delay = float('inf')
    #     new_delay = float('inf')
    #     runtime = 0.0
    #     forest_index = 0
    #     flow_edges = path_to_edges(self.__net.flows[foi].path)
        
    #     while True:
    #         start = time()
    #         timeout = floor(time_limit - runtime)
    #         if timeout <= 0:
    #             print(f'{cls}Timed out!-other')
    #             break

    #         prev_forest = deepcopy(self.__selected_edges)
    #         if not self.__next_forest(flow_edges, forest_index):
    #             print(f'{cls}Found the best (ecowcdb) delay!')
    #             break
    #         if prev_forest == self.__selected_edges and prev_forest != []:
    #             forest_index += 1
    #             continue
    #         print(f'{cls}Optimizing delay... (time left = {timeout}s)', end='')

    #         stdout.flush()

    #         # ONLY AVAILABLE IN UNIX!!!!
    #         # CAN USE Threading.Timer() maybe
    #         # don't waste time on timeout
    #         signal(SIGALRM, timeout_handler)
    #         alarm(timeout)

    #         try:
    #             new_delay = self.__delay(foi, timeout, self.__selected_edges)
    #         except LPError as lperror:
    #             # SHOULD I JUST SKIP A CUT IF THERE IS ERROR?
    #             # EXPLAIN PROBLEM REGARDING TIMEOUT ERRORS...
    #             # explain in documentation and maybe provide a message to the users
    #             print(lperror)
    #             forest_index += 1
    #         except TimeoutError:
    #             print(f'{cls}Timed out!')
    #             break
    #         else:
    #             forest_index += 1

    #         if new_delay < best_delay:
    #             best_delay = new_delay
    #             print(f'{cls}Delay bound improved: {10**6*best_delay:.2f} microseconds')

    #         end = time()
    #         runtime += (end - start)

        
    #     return best_delay
