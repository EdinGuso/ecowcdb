"""
 desc.
"""

from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

class ECOWCDB:
    
    def __init__(self, net: Network, temp_folder: str = '') -> None:
        self.__net = net
        self.__temp_folder = temp_folder


    def delay(self, foi: int) -> float:
        # consider scaling if there's an error
        # derive the heuristic algorithm for finding next cut to try and try it in a loop
        PLP = FifoLP(self.__net, list_edges=[], sfa=True, tfa=True, timeout=60, temp_folder=self.__temp_folder, filename="fifo", verbose=False)
        PLP.forest = PLP.forest.make_feed_forward()
        return PLP.delay(foi)
