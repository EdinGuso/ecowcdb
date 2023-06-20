"""
 desc.
"""

# Standard Library Imports
from math import floor
from time import time

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
    
    def __init__(self, net: Network, temp_folder: str = '') -> None:
        # self.__validation = Validation.ECOWCDB()
        self.__net = net
        self.__temp_folder = temp_folder

    def delay(self, foi: int, time_limit: int) -> float:
        # consider scaling if there's an error
        runtime = 0.0
        while runtime < time_limit:
            start = time()
            timeout = floor(time_limit - runtime)
            forest = [] # select forest heuristically
            try:
                PLP = FifoLP(self.__net, list_edges=forest, sfa=True, tfa=True, timeout=timeout, temp_folder=self.__temp_folder)
                PLP.forest = PLP.forest.make_feed_forward()
                return PLP.delay(foi)
            except LPError as lperror:
                pass
            
            end = time()
            runtime += (end - start)
