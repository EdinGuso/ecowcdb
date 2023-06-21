"""
 desc.
"""

# Standard Library Imports
from copy import deepcopy
from math import floor
from signal import alarm, signal, SIGALRM
from sys import stdout
from time import time
from typing import List, Tuple

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

# Local Imports - utility libraries
from ecowcdb.util.errors import LPError
from ecowcdb.util.network import is_forest, path_to_edges
# from ecowcdb.util.validation import Validation


class ECOWCDB:
    # __validation: Validation.ECOWCDB
    __net: Network
    __remaining_edges: List[Tuple[int, int]]
    __selected_edges: List[Tuple[int, int]]
    __temp_folder: str
    __PATH_RATE: List[float]
    __OTHER_RATE: List[float]
    
    def __init__(self, net: Network, temp_folder: str = '') -> None:
        # self.__validation = Validation.ECOWCDB()
        self.__net = net
        self.__temp_folder = temp_folder
        self.__PATH_RATE = [0.0, 0.35, 0.63, 0.85, 1.0] # open to discussion
        self.__OTHER_RATE = [0.3, 0.55, 0.75, 0.9, 1.0] # open to discussion

    def __next_forest(self, flow_edges: List[Tuple[int, int]], i: int) -> bool:
        # CAN I ASSUME THAT FLOWS DO NOT HAVE CYCLES??
        if i < len(self.__PATH_RATE):
            while len(self.__selected_edges) / len(flow_edges) < self.__PATH_RATE[i]:
                next_edge = flow_edges[len(self.__selected_edges)]
                self.__selected_edges += [next_edge]
                self.__remaining_edges.remove(next_edge)
        elif i < len(self.__PATH_RATE) + len(self.__OTHER_RATE):
            if len(self.__remaining_edges) == 0:
                return False
            edge_added = False
            while (len(self.__selected_edges) - len(flow_edges)) / (len(list(self.__net.edges.keys())) - len(flow_edges)) < self.__OTHER_RATE[i-len(self.__PATH_RATE)]:
                for edge in self.__remaining_edges:
                    if edge not in self.__selected_edges and edge[1] in [e[0] for e in self.__selected_edges]:
                        if is_forest(self.__net.decomposition(self.__selected_edges + [edge])[0]):
                            self.__selected_edges += [edge]
                            self.__remaining_edges.remove(edge)
                            edge_added = True
                            break
                if not edge_added or len(self.__remaining_edges) == 0:
                    return False
        else:
            print('ERROR: should never enter this condition')
            return False
        return True

    def __delay(self, foi: int, timeout: int, forest: List[Tuple[int, int]]) -> float:
        PLP = FifoLP(self.__net, list_edges=forest, sfa=True, tfa=True, timeout=timeout, temp_folder=self.__temp_folder)
        PLP.forest = PLP.forest.make_feed_forward()
        return PLP.delay(foi)

    def delay(self, foi: int, time_limit: int | float) -> float:
        def timeout_handler(signum, frame):
            raise TimeoutError("Function timed out.")
        cls = '\r' + ' '*50 + '\r'
        
        

        self.__remaining_edges = list(self.__net.edges.keys())
        self.__selected_edges = []

        best_delay = float('inf')
        new_delay = float('inf')
        runtime = 0.0
        forest_index = 0
        flow_edges = path_to_edges(self.__net.flows[foi].path)
        
        while True:
            start = time()
            timeout = floor(time_limit - runtime)
            if timeout <= 0:
                print(f'{cls}Timed out!-other')
                break

            prev_forest = deepcopy(self.__selected_edges)
            if not self.__next_forest(flow_edges, forest_index):
                print(f'{cls}Found the best (ecowcdb) delay!')
                break
            if prev_forest == self.__selected_edges and prev_forest != []:
                forest_index += 1
                continue
            print(f'{cls}Optimizing delay... (time left = {timeout}s)', end='')

            stdout.flush()

            signal(SIGALRM, timeout_handler)
            alarm(timeout)

            try:
                new_delay = self.__delay(foi, timeout, self.__selected_edges)
            except LPError as lperror:
                # SHOULD I JUST SKIP A CUT IF THERE IS ERROR?
                # EXPLAIN PROBLEM REGARDING TIMEOUT ERRORS...
                print(lperror)
                forest_index += 1
            except TimeoutError:
                print(f'{cls}Timed out!')
                break
            else:
                forest_index += 1

            if new_delay < best_delay:
                best_delay = new_delay
                print(f'{cls}Delay bound improved: {10**6*best_delay:.2f} microseconds')

            end = time()
            runtime += (end - start)

        
        return best_delay
