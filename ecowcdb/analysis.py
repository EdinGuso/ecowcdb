"""
 File containing the analysis tool.
"""

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
    """
     Class for analyzing networks. Can perform exhaustive search, partial search, and individual cut's delay analysis.
     After the analysis, the user can either display the results, save the results to a text file, or save the results
     object to a pickle file.
     
     Attributes:
         __validation (Validation, private): Validation object used to validate user inputs.
         __results (Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]], private): Dictionary which holds the
         computed results.
         __net (Network, private): The network object for which the analysis is performed.
         __forest_generation (ForestGeneration, private): Forest generation mode used.
         __forests (List[List[Tuple[int, int]]], private): Holds the generated forests.
         __timeout (int, private): Max timeout value provided by the user. This is the hard timeout limit.
         __delay_unit (DisplayUnit, private): Unit in which the delay values will be displayed in.
         __runtime_unit (DisplayUnit, private): Unit in which the runtime values will be displayed in.
         __temp_folder (str, private): Folderpath in which the .lp files will be stored in.
         __results_folder (str, private): Folderpath in which the results will be stored in.
         __verbose (List[VerboseKW], private): List of verbose keywords indicating how much feedback regarding internal
         processes will be displayed to the user.
         __total_runtime (float, private): The total runtime taken in the current exhaustive search.
         __num_iters (int, private): The total number of cuts analyzed in the current exhaustive search.
         __timeout_factor (int, private): Initial timeout factor. Average runtime is multiplied by this factor to
         determine the soft timeout limit. This factor is dynamically updated when necessary.
         __SCALE_FACTORS (List[float], private): The list of scaling factors to be applied to the network in terms of
         lp errors.
         __HEADER (List[Tuple[str, str, str, str]], private): Header of the table.
         __RESULTS_FILE_FORMAT (str, private): File extension of human readable results files.
         __RAW_FILE_FORMAT (str, private): File extension of the raw dump of the results.
     
     Methods:
         __compute_timeout (private): desc.
         delay (public): desc.
         __exhaustive_search_symmetric_copy (private): desc.
         __exhaustive_search_symmetric_cycle (private): desc.
         exhaustive_search (public): desc.
         exhaustive_search_all_flows (public): desc.
         __results_table (private): desc.
         display_results (public): desc.
         save_results (public): desc.
         save_raw_results (public): desc.
         load_raw_results (public): desc.
    """
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
    __timeout_factor: int
    __SCALE_FACTORS: List[float]
    __HEADER: List[Tuple[str, str, str, str]]
    __RESULTS_FILE_FORMAT: str
    __RAW_FILE_FORMAT: str

    def __init__(self, net: Network, forest_generation: ForestGeneration = ForestGeneration.All, num_forests: int = 0,
                 min_edges: int = 0, timeout: int = 600, delay_unit: DisplayUnit = DisplayUnit.Second,
                 runtime_unit: DisplayUnit = DisplayUnit.Second, temp_folder: str = '', results_folder: str = '',
                 verbose: List[VerboseKW] = []) -> None:
        """
        Initialize analysis. This function will validate all the inputs and generate everything needed to start the
        analysis.
        
         Args:
             net (Network, required): Network to analyze.
             forest_generation (ForestGeneration, optional): Specifies the type of forest generation to use. Default is
             ForestGeneration.All which means all valid forests are generated.
             num_forests (int, optional): Number of forests to generate. This is only used when the forest_generation
             is set to ForestGeneration.Partial. Default is 0 which means no forests will be generated.
             min_edges (int, optional): Minimum number of edges in generated forests. Default is 0 which means there is
             no restrictions on forest size.
             timeout (int, optional): Hard limit for timeout [seconds]. Every lp_solve call will be at most this long.
             Default is 600 [seconds].
             delay_unit (DisplayUnit, optional): Unit of time in which the delays will be displayed in the results
             table. Default is DelayUnit.Second.
             runtime_unit (DisplayUnit, optional): Unit of time in which the runtimes will be displayed in the results
             table. Default is DelayUnit.Second.
             temp_folder (str, optional): Folder to store temporary .lp files. It is the user's responsibility to
             ensure that the provided folder exists. Default is '' which means that temp files will be stored in the
             directory from where the intial call was made.
             results_folder (str, optional): Folder to store analysis results. It is the user's responsibility to
             ensure that the provided folder exists. Default is '' which means that results will be stored in the
             directory from where the intial call was made.
             verbose (List[VerboseKW], optional): List of verbosity options. Default is [] which means all options are
             disabled.
        """
        self.__validation = Validation.Analysis()
        self.__validation.constructor_arguments(net, forest_generation, num_forests, min_edges, timeout, delay_unit,
                                                runtime_unit, temp_folder, results_folder, verbose)
        self.__net = net
        self.__forest_generation = forest_generation
        self.__forests = generate_forests(net, forest_generation, min_edges, num_forests,
                                          True if VerboseKW.FG_ProgressBar in verbose else False)
        self.__timeout = timeout
        self.__delay_unit = delay_unit
        self.__runtime_unit = runtime_unit
        self.__temp_folder = temp_folder
        self.__results_folder = results_folder
        self.__verbose = verbose
        self.__results = {}
        self.__total_runtime = 0.0
        self.__num_iters = 0
        self.__timeout_factor = 2
        self.__SCALE_FACTORS = [1.0, 0.1, 10.0]
        self.__HEADER = generate_header(delay_unit, runtime_unit)
        self.__RESULTS_FILE_FORMAT = '.txt'
        self.__RAW_FILE_FORMAT = '.pickle'

        if VerboseKW.Network in self.__verbose:
            print(self.__net)

    def __compute_timeout(self, all_delays: bool) -> int:
        """
         Dynamic timeout computation method. This function is called before each delay computation.
         
         Args:
         	 all_delays (bool, required): If true delay is being computed for all the flows, and the timeout value will
             be properly scaled.
         
         Returns: 
         	 int: The timeout to use during the lp_solve calls in delay computation.
        """
        if self.__num_iters == 0:
            return self.__timeout
        average_runtime = self.__total_runtime / self.__num_iters
        upper_bound = ceil(average_runtime * self.__timeout_factor)
        if self.__timeout < upper_bound:
            return self.__timeout
        if all_delays:
            return upper_bound * self.__net.num_flows
        return upper_bound

    def delay(self, foi: int | None, forest: List[Tuple[int, int]], _internal_call: bool = False,
              _all_delays:bool = False) -> float | List[float]:
        """
         Compute the delay for a given forest. This function encapsulates all the interactions with the panco library.
         
         Args:
         	 foi (int | None, required): Flow of interest. None only if _all_delays is True.
         	 forest (List[Tuple[int, int]], required): List of edges representing the forest.
         	 _internal_call (bool, internal): This is an internal parameter and should not be changed by the user.
             Indicates whether the function was called internally. Default is False.
         	 _all_delays (bool, internal): This is an internal parameter and should not be changed by the user.
             Indicates whether all flow delays should be computed. Default is False.

         Raises:
             ValueError: If an unrecognized LPError is caught.
         
         Returns: 
         	 float | List[float]: The delay for the foi if _all_delays is False, list of delays for all flows if
             _all_delays is True. User should always expect a single float, not a list.
        """
        # If it is not an internal call, we need to check the user inputs.
        if not _internal_call:
            self.__validation.foi(foi, self.__net.num_flows)
            self.__validation.forest(forest, self.__net)

        if VerboseKW.Forest in self.__verbose:
            print(f'Computing delay for {forest=}')

        lp_verbose = True if VerboseKW.LP_Details in self.__verbose else False
        scale_factor_index = 0
        could_not_solve = False
        while not could_not_solve:
            scale_factor = self.__SCALE_FACTORS[scale_factor_index]
            scaled_net = scale_network(self.__net, scale_factor)
            timeout = self.__compute_timeout(_all_delays)
            PLP = FifoLP(scaled_net, list_edges=forest, sfa=True, tfa=True, timeout=timeout,
                         temp_folder=self.__temp_folder, filename="fifo", verbose=lp_verbose)
            PLP.forest = PLP.forest.make_feed_forward()
            try:
                if _all_delays:
                    return PLP.all_delays
                return PLP.delay(foi)
            except LPError as lperror:
                error_msg = ''
                if lperror.error_type() in [LPErrorType.AccuracyError, LPErrorType.TimeoutError,
                                            LPErrorType.LPSolveFailure]:
                    if scale_factor_index == len(self.__SCALE_FACTORS)-1:
                        error_msg = f'{lperror} encountered for {scale_factor=}. Could not solve after trying every \
                            scaling factor. Skipping this cut!'
                        could_not_solve = True
                    else:
                        error_msg = f'{lperror} encountered for {scale_factor=}. Rescaling the problem...'
                        scale_factor_index += 1
                elif lperror.error_type() in [LPErrorType.SuboptimalSolutionWarning]:
                    if timeout == self.__timeout:
                        error_msg = f'{lperror} encountered for {timeout=}. Maximum timeout reached. Skipping this \
                            cut!'
                        could_not_solve = True
                    else:
                        error_msg = f'{lperror} encountered for {timeout=}. Doubling the timeout value...'
                        self.__timeout_factor *= 2
                elif lperror.error_type() in [LPErrorType.InfeasibleProblemError, LPErrorType.UnboundedProblemError,
                                              LPErrorType.UnhandledLPError]:
                    error_msg = f'{lperror} encountered. Could not solve the LP. Skipping this cut!'
                    could_not_solve = True
                else:
                    raise ValueError(f'Unhandled error type: {lperror}.')
                
                if VerboseKW.LP_Errors in self.__verbose:
                    print(error_msg)

        # Return infinity if this cut has failed.
        return float('inf')
    
    # Copies the results obtained in exhaustive search to other flows
    def __exhaustive_search_symmetric_copy(self) -> None:
        """
         Copies the results of flow 0 to all other flows by offsetting the node indexes in edges. This is a helper
         function for __exhaustive_search_symmetric_cycle.
        """
        N = self.__net.num_flows
        for foi in range(1, N):
            # One-liner which offsets edges in the forest to obtain results of other flows.
            self.__results[foi]\
                = [(sorted([((edge[0]+foi)%N,(edge[1]+foi)%N) for edge in result[0]], key=lambda x: x[0]),
                    result[1], result[2]) for result in self.__results[0]]

    def __exhaustive_search_symmetric_cycle(self) -> None:
        """
         Exhaustive search for symmetric cycles. More efficient computation for a single flow by exploiting the fact
         that there are many symmetric forests. Computing results for a single flow and all flows is the same runtime.
         Therefore, even if the user asks for a single flow to be computed, all flows are computed.
        """
        result = []
        forests = self.__forests
        if VerboseKW.ES_ProgressBar in self.__verbose:
            forests = tqdm(
                iterable=self.__forests,
                desc=f'Symmetric cycle detected. Calculating delay bounds for all flows',
                unit='forest')

        pre_computed_forests = set()
        for forest in forests:
            # Check whether the result for that forest was computed by symmetricity in a previous iteration.
            if tuple(forest) in pre_computed_forests:
                pre_computed_forests.remove(tuple(forest))
                continue

            start = time()
            symmetric_forests = generate_symmetric_forests(forest, self.__net.num_servers)
            delays = self.delay(None, forest, _internal_call=True, _all_delays=True)
            end = time()
            elapsed = end - start
            for delay, symmetric_forest in zip(delays[:len(symmetric_forests)],
                                               [symmetric_forests[0]] + symmetric_forests[1:][::-1]):
                result.append((symmetric_forest, delay, elapsed/len(symmetric_forests)))
                pre_computed_forests.add(tuple(symmetric_forest))

            self.__total_runtime += elapsed
            self.__num_iters += len(symmetric_forests)
            pre_computed_forests.remove(tuple(forest))
        
        self.__total_runtime = 0.0
        self.__num_iters = 0
        self.__results[0] = sorted(result, key=lambda x: x[1])
        self.__exhaustive_search_symmetric_copy()

    def exhaustive_search(self, foi: int, _internal_call: bool = False) -> None:
        """
         Perform exhaustive search for the given flow over all forests in self.__forests. Saves results in
         self.__results.
         
         Args:
         	 foi (int, required): Flow of interest.
         	 _internal_call (bool, internal): This is an internal parameter and should not be changed by the user.
             Indicates whether the function was called internally. Default is False.
        """
        # If it is not an internal call, we need to check the user inputs.
        if not _internal_call:
            self.__validation.callable(self.__forest_generation, self.exhaustive_search)
            self.__validation.foi(foi, self.__net.num_flows)

        # If it is a symmetric cycle, we can perform the efficient exhaustive search.
        if self.__net.symmetric_cycle:
            self.__exhaustive_search_symmetric_cycle()
            return
        
        result = []
        forests = self.__forests
        if VerboseKW.ES_ProgressBar in self.__verbose:
            forests = tqdm(
                iterable=self.__forests,
                desc=f'Calculating delay bounds for flow {foi}',
                unit='forest')

        for forest in forests:
            start = time()
            delay = self.delay(foi, forest, _internal_call=True)
            end = time()
            elapsed = end - start
            result.append((forest, delay, elapsed))
            self.__total_runtime += elapsed
            self.__num_iters += 1
        
        self.__total_runtime = 0.0
        self.__num_iters = 0
        self.__results[foi] = sorted(result, key=lambda x: x[1])

    def exhaustive_search_all_flows(self) -> None:
        """
         Perform exhaustive search for all flows over all forests in self.__forests. Saves results in self.__results.
        """
        self.__validation.callable(self.__forest_generation, self.exhaustive_search_all_flows)

        # If it is a symmetric cycle, we can perform the efficient exhaustive search.
        if self.__net.symmetric_cycle:
            self.__exhaustive_search_symmetric_cycle()
            return

        for foi in range(self.__net.num_flows):
            self.exhaustive_search(foi, _internal_call=True)


    def __results_table(self, foi: int) -> str:
        """
         Returns a table of results for the flow of interest. It is formatted to be a human readable table. This is a
         helper function for display_results and save_results.
         
         Args:
         	 foi (int, requried): Flow of interest.
         
         Returns: 
         	 str: Results table
        """
        self.__validation.foi(foi, self.__net.num_flows)

        table = self.__HEADER + convert_result_units(self.__results[foi], self.__delay_unit, self.__runtime_unit)

        result = '########################\n'
        result += f'###Results for flow {foi}###\n'
        result += '########################\n'
        result += 'NOT COMPUTED!\n' if foi not in self.__results else tabulate(table,
                                                                               headers='firstrow',
                                                                               tablefmt='fancy_grid') + '\n'

        return result
    
    def display_results(self, foi: int) -> None:
        """
         Displays the results for the given flow of interest.
         
         Args:
         	 foi (int, requried): Flow of interest.
        """
        print(self.__results_table(foi))

    def save_results(self, foi: int, filename: str) -> None:
        """
         Saves the results for the given flow of interest to the given file.
         
         Args:
         	 foi (int, requried): Flow of interest.
         	 filename (str, required): Name of the file to save. The name should not include the extension as the
             extension is added automatically within the function.
        """
        self.__validation.filename(filename)
        filepath = self.__results_folder + filename + self.__RESULTS_FILE_FORMAT
        with open(filepath, "w") as file:
            print(self.__results_table(foi), file=file)

    def save_raw_results(self, filename: str) -> None:
        """
         Save the results object to the given file.
         Args:
         	 filename (str, required): Name of the file to save. The name should not include the extension as the
             extension is added automatically within the function.
        """
        self.__validation.filename(filename)
        filepath = self.__results_folder + filename + self.__RAW_FILE_FORMAT
        with open(filepath, 'wb') as file:
            dump(self.__results, file)

    def load_raw_results(self, filename: str) -> None:
        """
         Load results object from the given file.
         
         Args:
         	 filename (str, required): Name of the file to load. The name should not include the extension as the
             extension is added automatically within the function. It is user's responsibility to ensure that the given
             file exists.
        """
        self.__validation.filename(filename)
        filepath = self.__results_folder + filename + self.__RAW_FILE_FORMAT
        with open(filepath, 'rb') as file:
            self.__results = load(file)
