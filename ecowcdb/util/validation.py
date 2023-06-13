"""
 File containing the Validation classes. The classes and functions within this file perform strict user input
 validation to ensure a controlled environment within the analysis part of the code.
"""

# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit, ForestGeneration, NetworkType, VerboseKW

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network

# Local Imports - utility libraries
from ecowcdb.util.network import is_forest



class Validation:
    """
     Base class for user input validation classes.

     Methods:
         _type (protected): Validates that arg is of expected_types.
         _types_in_list (protected): Validates that all items in arg_list are of expected_types.
         _non_negative (protected): Validates that arg is non negative.
         _positive (protected): Validates that arg is positive.
         _upper_bound (protected): Validates that arg is less than upper_bound.
         _exists_in_dict (protected): Validates that arg exists in dict.
    """

    def _type(self, arg: Any, arg_name: str, expected_types: type | Tuple[type, ...]) -> None:
        """
         Validates that arg is of expected_types.
         
         Args:
         	 arg (Any, required): The argument to check.
         	 arg_name (str, required): The name of the argument for error messages.
         	 expected_types (type | Tuple[type, ...], required): The type or tuple of types arg is expected to be.
         
         Raises:
             TypeError: If arg is not of expected_types.
        """
        if not isinstance(arg, expected_types):
            raise TypeError(f'Argument \'{arg_name}\' must be of types {expected_types}, not {type(arg)}')
        
    def _types_in_list(self, arg_list: List[Any], arg_name: str, expected_types: type | Tuple[type, ...]) -> None:
        """
         Validates that all items in arg_list are of expected_types.
         
         Args:
         	 arg_list (List[Any], required): List of arguments to check.
         	 arg_name (str, required): The name of the argument for error messages.
         	 expected_types (type | Tuple[type, ...], required): The type or tuple of types arg is expected to be.
         
         Raises:
             TypeError: If any arg is not of expected_types.
        """
        for arg in arg_list:
            if not isinstance(arg, expected_types):
                raise TypeError(f'List argument \'{arg_name}\' can only contain items of types {expected_types},\
                                not {type(arg)}')

    def _non_negative(self, arg: int | float, arg_name: str) -> None:
        """
         Validates that arg is non negative.
         
         Args:
         	 arg (int | float, required): The argument to check.
         	 arg_name (str, required): The name of the argument for error messages.
         
         Raises:
             ValueError: If arg is negative.
        """
        if arg < 0:
            raise ValueError(f'Argument \'{arg_name}\' cannot be negative')
        
    def _positive(self, arg: int | float, arg_name: str) -> None:
        """
         Validates that arg is positive.
         
         Args:
         	 arg (int | float, required): The argument to check.
         	 arg_name (str, required): The name of the argument for error messages.
         
         Raises:
             ValueError: If arg is not positive.
        """
        if not arg > 0:
            raise ValueError(f'Argument \'{arg_name}\' must be positive')
        
    def _upper_bound(self, arg: int | float, arg_name: str, upper_bound: int | float) -> None:
        """
         Validates that arg is less than upper_bound.
         
         Args:
         	 arg (int | float, required): The argument to check.
         	 arg_name (str, required): The name of the argument for error messages.
         	 upper_bound (int | float, required): The upper bound for the argument.
         
         Raises:
             ValueError: If arg is larger than upper_bound.
        """
        if arg > upper_bound:
            raise ValueError(f'Argument \'{arg_name}\' cannot be larger than {upper_bound}')
        
    def _exists_in_dict(self, arg: Any, arg_name: str, dictionary: Dict[Any, Any]) -> None:
        """
         Validates that arg exists in dict.
         
         Args:
         	 arg (int | float, required): The argument to check.
         	 arg_name (str, required): The name of the argument for error messages.
         	 dictionary (Dict[Any, Any], required): The dict in which the argument is to be checked.
         
         Raises:
             ValueError: If arg is not in dictionary.
        """
        if arg not in dictionary:
            raise ValueError(f'Argument \'{arg_name}\' does not exist in dict')


    class Analysis:
        """
         Class that handles all the user input validation for Analysis class.

         Attributes:
             __validation (Validation, private): Base Validation object used to access generic validation functions.

         Methods:
             constructor_arguments (public): Validates all the arguments passed to the constructor of the Analysis
             class.
             callable (public): Checks whether a given function is callable.
             foi (public): Validates the given foi.
             forest (public): Validates the given forest.
             index (public): Validates the given index.
             indexes (public): Validates given indexes.
             filename (public): Validates the given filename.
        """
        # __validation: Validation

        def __init__(self) -> None:
            """
             Initialize the Validation.Analysis object. This is the constructor for the class.
            """
            self.__validation = Validation()
        
        def constructor_arguments(self, net: Network, forest_generation: ForestGeneration, num_forests: int,
                                  min_edges: int, timeout: int, delay_unit: DisplayUnit, runtime_unit: DisplayUnit,
                                  temp_folder: str, results_folder: str, verbose: List[VerboseKW]) -> None:
            """
             Validates all the arguments passed to the constructor of the Analysis class.
             
             Args:
             	 net (Network, required): Network to be validated.
             	 forest_generation (ForestGeneration, required): ForestGeneration to be validated.
             	 num_forests (int, required): int to be validated.
             	 min_edges (int, required): int to be validated.
             	 timeout (int, required): int to be validated.
             	 delay_unit (DisplayUnit, required): DisplayUnit to be validated.
             	 runtime_unit (DisplayUnit, required): DisplayUnit to be validated.
             	 temp_folder (str, required): str to be validated.
             	 results_folder (str, required): str to be validated.
             	 verbose (List[VerboseKW], required): List of VerboseKW to be validated.
            """
            self.__validation._type(net, 'net', Network)
            self.__validation._type(forest_generation, 'forest_generation', ForestGeneration)
            self.__validation._type(num_forests, 'num_forests', int)
            self.__validation._type(min_edges, 'min_edges', int)
            self.__validation._type(timeout, 'timeout', int)
            self.__validation._type(delay_unit, 'delay_unit', DisplayUnit)
            self.__validation._type(runtime_unit, 'runtime_unit', DisplayUnit)
            self.__validation._type(temp_folder, 'temp_folder', str)
            self.__validation._type(results_folder, 'results_folder', str)
            self.__validation._type(verbose, 'verbose', list)
            self.__validation._non_negative(num_forests, 'num_forests')
            self.__validation._non_negative(min_edges, 'min_edges')
            self.__validation._upper_bound(min_edges, 'min_edges', len(list(net.edges.keys())))
            self.__validation._positive(timeout, 'timeout')
            self.__validation._types_in_list(verbose, 'verbose', VerboseKW)

        def callable(self, forest_generation: ForestGeneration, foo: Callable[..., Any]) -> None:
            """
             Checks whether a given function is callable. This function is called only from relevant functions and
             the result depends only on the value of forest_generation 
             
             Args:
             	 forest_generation (ForestGeneration, required): Type of forest generation used in the analysis.
             	 foo (Callable[..., Any], required): The function that depends on forest generation.
             
             Raises: 
             	 ValueError: If forest generation was set to empty mode.
            """
            if forest_generation == ForestGeneration.Empty:
                raise ValueError(f'Cannot execute function \'{foo.__name__}\' because argument \'forest_generation\'\
                                 option was set to {ForestGeneration.Empty} in the constructor')

        def foi(self, foi: int | None, num_flows: int, all_delays: bool) -> None:
            """
             Validates the given foi. Checks if it is an int, non-negative, and less than the largest possible flow.
             
             Args:
                 foi (int | None, required): Flow of interest to be validated. None if all_delays is True.
             	 num_flows (int, required): The number of flows in the network.
             	 all_delays (bool, required): Indicates whether all_delays are being computed.
             
             Raises: 
             	 ValueError: If foi is not None when all_delays is True.
            """
            if all_delays:
                if foi is not None:
                    raise ValueError(f'Argument \'foi\' must be {None} when argument \'all_delays\' is set to {True}')
                return
            self.__validation._type(foi, 'foi', int)
            self.__validation._non_negative(foi, 'foi')
            self.__validation._upper_bound(foi, 'foi', num_flows-1)

        def forest(self, forest: List[Tuple[int, int]], net: Network) -> None:
            """
             Validates the given forest. Checks that every edge in the forest is a valid edge and it is a valid forest.
             
             Args:
                 forest (List[Tuple[int, int]], required): Forest to be validated.
                 net (Network, required): The network this forest belongs to.
             
             Raises: 
             	 ValueError: If any edge in the forest is not a valid edge or if the forest is not a valid forest.
            """
            self.__validation._type(forest, 'forest', list)
            for edge in forest:
                if edge not in list(net.edges.keys()):
                    raise ValueError(f'Edges within \'forest\' must be valid edges of this network')
            if not is_forest(net.decomposition(forest)[0]):
                raise ValueError(f'Argument \'forest\' is not a valid forest')

        def index(self, index: int, forests: List[List[Tuple[int, int]]]) -> None:
            """
             Validates the given index. Checks if it is an int, non-negative, and less than the number of forests.
             
             Args:
                 index (int, required): Index to be validated.
             	 forests (List[List[Tuple[int, int]]], required): All forests generated for this analysis.
            """
            self.__validation._type(index, 'index', int)
            self.__validation._non_negative(index, 'index')            
            self.__validation._upper_bound(index, 'index', len(forests)-1)            
            
        def indexes(self, indexes: List[int]) -> None:
            """
             Validates given indexes. Checks if it is a list.

             Args:
                 indexes (List[int], required): Indexes to be validated.
            """
            self.__validation._type(indexes, 'indexes', list)
            
        def filename(self, filename: str) -> None:
            """
             Validates the given filename. Checks if it is a str.
             
             Args: 
             	 filename (str, required): Filename to be validated
            """
            self.__validation._type(filename, 'filename', str)
            
            
    class Stats:
        """
         Class that handles all the user input validation for Stats class.

         Attributes:
             __validation (Validation, private): Base Validation object used to access generic validation functions.

         Methods:
             constructor_arguments (public): Validates all the arguments passed to the constructor of the Stats class.
             foi (public): Validates the given foi.
        """
        # __validation: Validation

        def __init__(self) -> None:
            """
             Initialize the Validation.Analysis object. This is the constructor for the class.
            """
            self.__validation = Validation()
        
        def constructor_arguments(self, results_folder: str, filename: str) -> None:
            """
             Validates all the arguments passed to the constructor of the Stats class.
             
             Args:
             	 results_folder (str, required): str to be validated.
             	 filename (str, required): str to be validated.
            """
            self.__validation._type(results_folder, 'results_folder', str)
            self.__validation._type(filename, 'filename', str)

        def foi(self, foi: int, results: Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]]) -> None:
            """
             Validates the given foi. Checks if it is an int, non-negative, and exists within the results.
             
             Args:
                 foi (int, required): Flow of interest to be validated.
             	 results (Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]], required): All the results.
            """
            self.__validation._type(foi, 'foi', int)
            self.__validation._non_negative(foi, 'foi')
            self.__validation._exists_in_dict(foi, 'foi', results)
            

    class Networks:
        """
         Class that handles all the user input validation for Networks class.

         Attributes:
             __validation (Validation, private): Base Validation object used to access generic validation functions.

         Methods:
             generic_arguments (public): Validates all the arguments passed to the constructor of the Stats class.
             foi (public): Validates the given foi.
        """
        # __validation: Validation
        
        def __init__(self) -> None:
            """
             Initialize the Validation.Analysis object. This is the constructor for the class.
            """
            self.__validation = Validation()

        def generic_arguments(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> None:
            """
             Validates all the arguments passed to the generic constructors of the Networks class.
             
             Args:
             	 R (float, required): float to be validated.
             	 L (float, required): float to be validated.
             	 S (float, required): float to be validated.
             	 N (int, required): int to be validated.
             	 load (float, required): float to be validated.
                 network_type (NetworkType, required): NetworkType to be validated
            """
            self.__validation._type(R, 'R', (int, float))
            self.__validation._type(L, 'L', (int, float))
            self.__validation._type(S, 'S', (int, float))
            self.__validation._type(N, 'N', int)
            self.__validation._type(load, 'load', float)
            self.__validation._type(network_type, 'network_type', NetworkType)
            self.__validation._positive(R, 'R')
            self.__validation._positive(L, 'L')
            self.__validation._positive(S, 'S')
            self.__validation._positive(N, 'N')
            self.__validation._positive(load, 'load')
            self.__validation._upper_bound(load, 'load', 1.0)
