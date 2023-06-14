# Standard Library Imports
from pickle import dump, load
from math import ceil
from time import time
from typing import Dict, List, Tuple

# Third-Party Library Imports
from tabulate import tabulate
from tqdm import tqdm

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit, ForestGeneration, VerboseKW

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.fifo.fifoLP import FifoLP

# Local Imports - utility libraries
from ecowcdb.util.errors import LPError, LPErrorType
from ecowcdb.util.network import generate_forests, generate_symmetric_forests, scale_network
from ecowcdb.util.units import convert_result_units, generate_header
from ecowcdb.util.validation import Validation



class Analysis:

    __validation: Validation.Analysis
    __results: Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]]
    __net: Network
    __forest_generation: ForestGeneration
    __forests: List[List[Tuple[int, int]]]
    __timeout: int
    __delay_unit: DisplayUnit
    __runtime_unit: DisplayUnit
    __temp_folder: str
    __results_folder: str
    __verbose: List[VerboseKW]
    __total_runtime: float
    __num_iters: int
    __timeout_factor_index: int
    __SCALE_FACTORS: List[float]
    __TIMEOUT_FACTORS: List[float]
    __HEADER: List[Tuple[str, str, str]]
    __RESULTS_FILE_FORMAT: str
    __RAW_FILE_FORMAT: str



    def __init__(self, net: Network, forest_generation: ForestGeneration = ForestGeneration.All, num_forests: int = 0, min_edges: int = 0,
                 timeout: int = 600, delay_unit: DisplayUnit = DisplayUnit.Second, runtime_unit: DisplayUnit = DisplayUnit.Second,
                 temp_folder: str = '', results_folder: str = '', verbose: List[VerboseKW] = []
                 ) -> None:
        self.__validation = Validation.Analysis()
        self.__validation.constructor_arguments(net, forest_generation, num_forests, min_edges, timeout, delay_unit, runtime_unit, temp_folder, results_folder, verbose)
        self.__net = net
        self.__forest_generation = forest_generation
        self.__forests = generate_forests(net, forest_generation, min_edges, num_forests)
        self.__timeout = timeout
        self.__delay_unit = delay_unit
        self.__runtime_unit = runtime_unit
        self.__temp_folder = temp_folder
        self.__results_folder = results_folder
        self.__verbose = verbose
        self.__results = {}
        self.__total_runtime = 0.0
        self.__num_iters = 0
        self.__timeout_factor_index = 0
        self.__SCALE_FACTORS = [1.0, 0.1, 10.0] # open to discussion
        self.__TIMEOUT_FACTORS = [3.0, 10.0, 50.0] # open to discussion
        self.__HEADER = generate_header(delay_unit, runtime_unit)
        self.__RESULTS_FILE_FORMAT = '.txt'
        self.__RAW_FILE_FORMAT = '.pickle'

        if VerboseKW.Network in self.__verbose:
            print(self.__net)

    def __compute_timeout(self, timeout_factor: float, all_delays: bool) -> int:
        if self.__num_iters == 0:
            return self.__timeout
        average_runtime = self.__total_runtime / self.__num_iters
        upper_bound = ceil(average_runtime * timeout_factor)
        if self.__timeout < upper_bound:
            return self.__timeout
        if all_delays:
            return upper_bound * self.__net.num_servers
        return upper_bound

        """_summary_

        Args:
            foi (int | None): _description_
            forest (List[Tuple[int, int]]): _description_
            _internal_call (bool, internal/private): _description_. Defaults to False.
            _all_delays (bool, internal/private): _description_. Defaults to False.

        Raises:
            ValueError: _description_

        Returns:
            float | List[float]: _description_
        """


    # encapsulates all the interactions with the panco library
    def delay(self, foi: int | None, forest: List[Tuple[int, int]], _internal_call: bool = False, _all_delays:bool = False) -> float | List[float]:
        
        self.__validation.foi(foi, self.__net.num_flows, _all_delays)
        if not _internal_call:
            self.__validation.forest(forest, self.__net)

        if VerboseKW.Forest in self.__verbose:
            print(f'Computing delay for {forest=}')

        lp_verbose = True if VerboseKW.LPProgress in self.__verbose else False
        scale_factor_index = 0
        could_not_solve = False
        while not could_not_solve:
            scale_factor = self.__SCALE_FACTORS[scale_factor_index]
            timeout_factor = self.__TIMEOUT_FACTORS[self.__timeout_factor_index]
            scaled_net = scale_network(self.__net, scale_factor)
            timeout = self.__compute_timeout(timeout_factor, _all_delays)
            PLP = FifoLP(scaled_net, list_edges=forest, sfa=True, tfa=True,
                         timeout=timeout, temp_folder=self.__temp_folder, filename="fifo", verbose=lp_verbose)
            PLP.forest = PLP.forest.make_feed_forward()
            try:
                if _all_delays:
                    return PLP.all_delays
                return PLP.delay(foi)
            except LPError as lperror:
                match lperror.error_type():
                    case LPErrorType.AccuracyError:
                        if VerboseKW.LPErrorMsg in self.__verbose:
                            print(f'{lperror} encountered for {scale_factor=}. Rescaling the problem...')
                        scale_factor_index += 1
                    case LPErrorType.TimeoutError:
                        if VerboseKW.LPErrorMsg in self.__verbose:
                            print(f'{lperror} encountered for {scale_factor=}. Rescaling the problem...')
                        scale_factor_index += 1
                    case LPErrorType.SuboptimalSolutionWarning:
                        if VerboseKW.LPErrorMsg in self.__verbose:
                            if timeout == self.__timeout:
                                print(f'{lperror} encountered for {timeout=}. Maximum timeout reached')
                                self.__timeout_factor_index = len(self.__TIMEOUT_FACTORS)
                            else:
                                print(f'{lperror} encountered for {timeout=}. Increasing the timeout value...')
                                self.__timeout_factor_index += 1
                    case _:
                        raise ValueError(f'Unhandled error type: {lperror}')
                if scale_factor_index >= len(self.__SCALE_FACTORS) or self.__timeout_factor_index >= len(self.__TIMEOUT_FACTORS):
                    self.__timeout_factor_index -= 1
                    could_not_solve = True

        if VerboseKW.LPErrorMsg in self.__verbose:
            print('Could not solve the LP! Skipping this cut')

        return float('inf')

    # allows the user to call compute the delay of a specific forest based on index
    def delay_by_index(self, foi: int, index: int) -> float:

        self.__validation.callable(self.__forest_generation, self.delay_by_index)
        self.__validation.index(index, self.__forests)
        
        return self.delay(foi, self.__forests[index], _internal_call=True)
    
    # allows the user to call compute the delay of specific forests based on indexes
    def delay_by_indexes(self, foi: int, indexes: List[int]) -> List[float]:

        self.__validation.callable(self.__forest_generation, self.delay_by_indexes)
        self.__validation.indexes(indexes)

        delays: List[float] = []

        for index in indexes:
            delays.append(self.delay_by_index(foi, index))

        return delays

    # perform exhaustive search over all possible cuts for the given flow
    def exhaustive_search(self, foi: int) -> None:

        self.__validation.callable(self.__forest_generation, self.exhaustive_search)
        
        result: List[Tuple[List[Tuple[int, int]], float, float]] = []

        iterable = tqdm(iterable=self.__forests, desc=f'Calculating delay bounds for flow {foi}', unit='forest') if VerboseKW.ProgressBar in self.__verbose else self.__forests

        for forest in iterable:

            start = time()

            delay = self.delay(foi, forest, _internal_call=True)
            
            end = time()

            elapsed = end - start

            result.append((forest, delay, elapsed))
            self.__total_runtime += elapsed
            self.__num_iters += 1
        
        self.__results[foi] = sorted(result, key=lambda x: x[1])

    # Copies the results obtained in exhaustive search to other flows
    def __exhaustive_search_symmetric_copy(self) -> None:
        N = self.__net.num_flows
        for foi in range(1, N):
            self.__results[foi] = [(sorted([((edge[0]+foi)%N,(edge[1]+foi)%N) for edge in result[0]], key=lambda x: x[0]), result[1], result[2]) for result in self.__results[0]]


    # Always computes for foi = 0 first because it is symmetric anyway and we copy results
    def __exhaustive_search_symmetric_cycle(self) -> None:
        result: List[Tuple[List[Tuple[int, int]], float, float]] = []
        iterable = tqdm(iterable=self.__forests, desc=f'Calculating delay bounds for all flows', unit='forest') if VerboseKW.ProgressBar in self.__verbose else self.__forests

        pre_computed_forests = set()
        for forest in iterable:
            if tuple(forest) in pre_computed_forests:
                pre_computed_forests.remove(tuple(forest))
                continue

            start = time()

            symmetric_forests = generate_symmetric_forests(forest, self.__net.num_servers)

            delays = self.delay(None, forest, _internal_call=True, _all_delays=True)
            
            end = time()

            elapsed = end - start

            for delay, symmetric_forest in zip(delays[:len(symmetric_forests)], [symmetric_forests[0]] + symmetric_forests[1:][::-1]):
                result.append((symmetric_forest, delay, elapsed/len(symmetric_forests)))
                pre_computed_forests.add(tuple(symmetric_forest))

            self.__total_runtime += elapsed
            self.__num_iters += len(symmetric_forests)
            pre_computed_forests.remove(tuple(forest))
        
        self.__results[0] = sorted(result, key=lambda x: x[1])
        self.__exhaustive_search_symmetric_copy()


    # perform exhaustive search over all possible cuts for all the flows
    def exhaustive_search_all_flows(self, all_flows_symmetric: bool = False) -> None:

        self.__validation.callable(self.__forest_generation, self.exhaustive_search_all_flows)

        if all_flows_symmetric:
            self.__exhaustive_search_symmetric_cycle()
            return

        for foi in range(self.__net.num_flows):
            self.exhaustive_search(foi)


    def __results_table(self, foi: int) -> str:

        self.__validation.foi(foi, self.__net.num_flows, False)

        table = self.__HEADER + convert_result_units(self.__results[foi], self.__delay_unit, self.__runtime_unit)

        result = '########################\n'
        result += f'###Results for flow {foi}###\n'
        result += '########################\n'
        result += 'NOT COMPUTED!\n' if foi not in self.__results else tabulate(table, headers='firstrow', tablefmt='fancy_grid') + '\n'

        return result
    
    # display the results fot the given foi
    def display_results(self, foi: int) -> None:

        print(self.__results_table(foi))

    def display_all_results(self) -> None:

        # does not work when loading a file, and initing with empty network
        for foi in range(self.__net.num_flows):
            self.display_results(foi)

    def save_results(self, foi: int, filename: str) -> None:

        self.__validation.filename(filename)

        filepath = self.__results_folder + filename + self.__RESULTS_FILE_FORMAT

        with open(filepath, "a") as file:
            print(self.__results_table(foi), file=file)

    def save_all_results(self, filename: str) -> None:

        # does not work when loading a file, and initing with empty network
        for foi in range(self.__net.num_flows):
            self.save_results(foi, filename)

    def save_raw_results(self, filename: str) -> None:

        self.__validation.filename(filename)

        filepath = self.__results_folder + filename + self.__RAW_FILE_FORMAT

        with open(filepath, 'wb') as file:
            dump(self.__results, file)

    def load_raw_results(self, filename: str) -> None:

        self.__validation.filename(filename)

        filepath = self.__results_folder + filename + self.__RAW_FILE_FORMAT

        with open(filepath, 'rb') as file:
            self.__results = load(file)
