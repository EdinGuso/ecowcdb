# Standard Library Imports
from typing import Any, Callable, Dict, List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit, ForestGeneration, NetworkType, VerboseKW

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network

# Local Imports - utility libraries
from ecowcdb.util.network import is_forest



class Validation:
    def _type(self, arg: Any, arg_name: str, expected_types: type | Tuple[type, ...]):
        if not isinstance(arg, expected_types):
            raise TypeError(f'Argument \'{arg_name}\' must be of types {expected_types}, not {type(arg)}')
        
    def _types_in_list(self, arg_list: List[Any], arg_name: str, expected_types: type | Tuple[type, ...]):
        for arg in arg_list:
            if not isinstance(arg, expected_types):
                raise TypeError(f'List argument \'{arg_name}\' can only contain items of types {expected_types}, not {type(arg)}')

    def _non_negative(self, arg: int | float, arg_name: str):
        if arg < 0:
            raise ValueError(f'Argument \'{arg_name}\' cannot be negative')
        
    def _positive(self, arg: int | float, arg_name: str):
        if not arg > 0:
            raise ValueError(f'Argument \'{arg_name}\' must be positive')
        
    def _upper_bound(self, arg: int | float, arg_name: str, upper_bound: int | float):
        if arg > upper_bound:
            raise ValueError(f'Argument \'{arg_name}\' cannot be larger than {upper_bound}')
        
    def _exists_in_dict(self, arg: Any, arg_name: str, container: Dict[Any, Any]):
        if arg not in container:
            raise ValueError(f'Argument \'{arg_name}\' does not exist in dict')


    class Analysis:
        def __init__(self) -> None:
            self.__validation = Validation()
        
        def constructor_arguments(self, net: Network, forest_generation: ForestGeneration, num_forests: int, min_edges: int, timeout: int, delay_unit: DisplayUnit, runtime_unit: DisplayUnit, temp_folder: str, results_folder: str, verbose: List[VerboseKW]) -> None:
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
            if forest_generation == ForestGeneration.Empty:
                raise ValueError(f'Cannot execute function \'{foo.__name__}\' because argument \'forest_generation\' option was set to {ForestGeneration.Empty} in the constructor')

        def foi(self, foi: int | None, num_flows: int, all_delays: bool) -> None:
            if all_delays:
                if foi is not None:
                    raise ValueError(f'Argument \'foi\' must be {None} when argument \'all_delays\' is set to {True}')
                return
            self.__validation._type(foi, 'foi', int)
            self.__validation._non_negative(foi, 'foi')
            self.__validation._upper_bound(foi, 'foi', num_flows-1)

        def forest(self, forest: List[Tuple[int, int]], net: Network) -> None:
            self.__validation._type(forest, 'forest', list)
            for edge in forest:
                if edge not in list(net.edges.keys()):
                    raise ValueError(f'Edges within \'forest\' must be valid edges of this network')
            if not is_forest(net.decomposition(forest)[0]):
                raise ValueError(f'Argument \'forest\' is not a valid forest')

        def index(self, index: int, forests: List[List[Tuple[int, int]]]) -> None:
            self.__validation._type(index, 'index', int)
            self.__validation._non_negative(index, 'index')            
            self.__validation._upper_bound(index, 'index', len(forests)-1)            
            
        def indexes(self, indexes: List[int]) -> None:
            self.__validation._type(indexes, 'indexes', list)
            
        def filename(self, filename: str) -> None:
            self.__validation._type(filename, 'filename', str)
            
            
    class Stats:
        def __init__(self) -> None:
            self.__validation = Validation()
        
        def constructor_arguments(self, results_folder: str, filename: str) -> None:
            self.__validation._type(results_folder, 'results_folder', str)
            self.__validation._type(filename, 'filename', str)

        def foi(self, foi: int, results: Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]]) -> None:
            self.__validation._type(foi, 'foi', int)
            self.__validation._non_negative(foi, 'foi')
            self.__validation._exists_in_dict(foi, 'foi', results)
            

    class Networks:
        def __init__(self) -> None:
            self.__validation = Validation()

        def generic_arguments(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> None:
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


