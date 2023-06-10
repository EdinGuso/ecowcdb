# Standard Library Imports
from pickle import dump, load
from time import time
from typing import List, Tuple

# Third-Party Library Imports
from tabulate import tabulate
from tqdm import tqdm

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit, VerboseKW

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

# Local Imports - utility libraries
from ecowcdb.util.errors import LPError
from ecowcdb.util.network import all_forests, scale_network
from ecowcdb.util.units import convert_result_units, generate_header
from ecowcdb.util.validation import Validation



class Analysis:

    def __init__(self, net: Network, generate_forests: bool = True, min_edges: int = 0, timeout: int = 600,
                 delay_unit: DisplayUnit = DisplayUnit.Second, runtime_unit: DisplayUnit = DisplayUnit.Second,
                 temp_folder: str = '', results_folder: str = '', verbose: List[VerboseKW] = []
                 ) -> None:
        self._validaton = Validation.Analysis()
        self._validaton.constructor_arguments(net, generate_forests,min_edges, timeout, delay_unit, runtime_unit, temp_folder, results_folder, verbose)
        self._net = net
        self._forests = all_forests(net, min_edges) if generate_forests else []
        self._timeout = timeout
        self._total_runtime = 0
        self._num_iters = 0
        self._generate_forests = generate_forests
        self._delay_unit = delay_unit
        self._runtime_unit = runtime_unit
        self._temp_folder = temp_folder
        self._results_folder = results_folder
        self._verbose = verbose
        self._results = {}
        self._HEADER = generate_header(delay_unit, runtime_unit)
        self._SCALE_FACTORS = [1, 10**-1, 10**-2, 10**-3, 10**-4, 10**-5, 10**-6, 10**1, 10**2, 10**3, 10**4, 10**5, 10**6] # open to discussion
        self._RESULTS_FILE_FORMAT = '.txt'
        self._RAW_FILE_FORMAT = '.pickle'

        if VerboseKW.Network in self._verbose:
            print(self._net)

    # encapsulates all the interactions with the panco library
    # accessed from outside and has the additional validate_forest function call
    def delay(self, foi: int, forest: List[Tuple[int, int]], _internal_call: bool = False) -> float:

        self._validaton.foi(foi, self._net.num_flows)
        if not _internal_call:
            self._validaton.forest(forest, list(self._net.edges.keys()))

        if VerboseKW.Forest in self._verbose:
            print(f'Computing delay for {forest=}')

        lp_verbose = True if VerboseKW.LPProgress in self._verbose else False

        for scale_factor in self._SCALE_FACTORS:
            try:
                scaled_net = scale_network(self._net, scale_factor)
                PLP = FifoLP(scaled_net, list_edges=forest, sfa=True, tfa=True, timeout=self._timeout, temp_folder=self._temp_folder, filename="fifo", verbose=lp_verbose)
                PLP.forest = PLP.forest.make_feed_forward()
                return PLP.delay(foi)
            except LPError as lperror:
                if VerboseKW.LPErrorMsg in self._verbose:
                    print(f'{lperror} encountered for {scale_factor=}. Rescaling the problem...')

        raise StopIteration('Failed to solve the LP after trying all the scaling factors')

    # allows the user to call compute the delay of a specific forest based on index
    def delay_by_index(self, foi: int, index: int) -> float:

        self._validaton.callable(self._generate_forests, self.delay_by_index)
        self._validaton.index(index, self._forests)
        
        return self.delay(foi, self._forests[index], _internal_call=True)
    
    # allows the user to call compute the delay of specific forests based on indexes
    def delay_by_indexes(self, foi: int, indexes: List[int]) -> List[float]:

        self._validaton.callable(self._generate_forests, self.delay_by_indexes)
        self._validaton.indexes(indexes)

        delays = []

        for index in indexes:
            delays.append(self.delay_by_index(foi, index))

        return delays

    # perform exhaustive search over all possible cuts for the given flow
    def exhaustive_search(self, foi: int) -> None:

        self._validaton.callable(self._generate_forests, self.exhaustive_search)
        
        result = []

        for forest in tqdm(iterable=self._forests, desc=f'Calculating delay bounds for flow {foi}', unit='forest'):

            start = time()

            delay = self.delay(foi, forest, _internal_call=True)
            
            end = time()

            elapsed = end - start

            result.append((forest, delay, elapsed))
            self._total_runtime += elapsed
            self._num_iters += 1
        
        self._results[foi] = sorted(result, key=lambda x: x[1])

    # perform exhaustive search over all possible cuts for all the flows
    def exhaustive_search_all_flows(self) -> None:

        self._validaton.callable(self._generate_forests, self.exhaustive_search_all_flows)

        for foi in range(self._net.num_flows):
            self.exhaustive_search(foi)

    def _results_table(self, foi: int) -> str:

        # Not validating foi due to error with empty network

        table = self._HEADER + convert_result_units(self._results[foi], self._delay_unit, self._runtime_unit)

        result = '########################\n'
        result += f'###Results for flow {foi}###\n'
        result += '########################\n'
        result += 'NOT COMPUTED!\n' if foi not in self._results else tabulate(table, headers='firstrow', tablefmt='fancy_grid') + '\n'

        return result
    
    # display the results fot the given foi
    def display_results(self, foi: int) -> None:

        print(self._results_table(foi))

    def display_all_results(self) -> None:

        for foi in range(self._net.num_flows):
            self.display_results(foi)

    def save_results(self, foi: int, filename: str) -> None:

        self._validaton.filename(filename)

        filepath = self._results_folder + filename + self._RESULTS_FILE_FORMAT

        with open(filepath, "a") as file:
            print(self._results_table(foi), file=file)

    def save_all_results(self, filename: str) -> None:

        for foi in range(self._net.num_flows):
            self.save_results(foi, filename)

    def save_raw_results(self, filename: str) -> None:

        self._validaton.filename(filename)

        filepath = self._results_folder + filename + self._RAW_FILE_FORMAT

        with open(filepath, 'wb') as file:
            dump(self._results, file)

    def load_raw_results(self, filename: str) -> None:

        self._validaton.filename(filename)

        filepath = self._results_folder + filename + self._RAW_FILE_FORMAT

        with open(filepath, 'rb') as file:
            self._results = load(file)
