"""
 desc.
"""

# Standard Library Imports
from math import floor
from time import time
from typing import List, Tuple

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

# Local Imports - utility libraries
from ecowcdb.util.errors import LPError, LPErrorType
from ecowcdb.util.network import scale_network
# from ecowcdb.util.validation import Validation


class ECOWCDB:
    # __validation: Validation.ECOWCDB
    __net: Network
    __temp_folder: str
    __done: bool
    __scale_factor: float
    __num_tries: int
    
    def __init__(self, net: Network, temp_folder: str = '') -> None:
        # self.__validation = Validation.ECOWCDB()
        self.__net = net
        self.__temp_folder = temp_folder
        self.__done = False
        self.__scale_factor = 1.0
        self.__num_tries = 4

    def __next_forest(self, i: int) -> List[Tuple[int, int]]:
        # HEURISTIC FOREST PICK - TO BE IMPLEMENTED
        if i == 0:
            return []
        if i == 1:
            return [(0,1),(1,2),(2,3),(3,4)]
        if i == 2:
            return [(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8)]
        if i == 3:
            return [(0,1),(1,2),(2,3),(3,4),(4,5),(5,6),(6,7),(7,8),(8,9),(9,10),(10,11)]

    def __delay(self, foi: int, timeout: int, forest: List[Tuple[int, int]]) -> float:
        PLP = FifoLP(self.__net, list_edges=forest, sfa=True, tfa=True, timeout=timeout, temp_folder=self.__temp_folder)
        PLP.forest = PLP.forest.make_feed_forward()
        return PLP.delay(foi)

    def delay(self, foi: int, time_limit: float) -> float:
        best_delay = float('inf')
        new_delay = float('inf')
        runtime = 0.0
        forest_index = 0
        while runtime < time_limit and not self.__done:
            start = time()
            timeout = floor(time_limit - runtime)
            print(f'Calculating delay... (time left = {timeout}s)', end='\n')
            # print('\r', end='')
            if timeout == 0:
                break
            forest = self.__next_forest(forest_index)
            try:
                new_delay = self.__delay(foi, timeout, forest)
            except LPError as lperror:
                print(lperror)
                if lperror.error_type() in [LPErrorType.AccuracyError, LPErrorType.TimeoutError, LPErrorType.LPSolveFailure]:
                    self.__scale_factor *= 0.1
                    self.__net = scale_network(self.__net, self.__scale_factor)
                else:
                    self.__done = True
            else:
                if new_delay < best_delay:
                    best_delay = new_delay
                    print(f'Delay bound improved: {10**6*best_delay}microseconds')
                forest_index += 1
                if forest_index == self.__num_tries:
                    self.__done = True
            
            end = time()
            runtime += (end - start)

        return best_delay
