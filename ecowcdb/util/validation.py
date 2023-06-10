# Standard Library Imports
from typing import Any, Callable, List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import DisplayUnit, VerboseKW

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network



class Validation:
    def _type(self, arg: Any, arg_name: str, expected_type: type):
        if not isinstance(arg, expected_type):
            raise TypeError(f'Argument \'{arg_name}\' must be of type {expected_type}, not {type(arg)}')
        
    def _types_in_list(self, arg_list: List[Any], arg_name: str, expected_type: type):
        for arg in arg_list:
            if not isinstance(arg, expected_type):
                raise TypeError(f'List argument \'{arg_name}\' can only contain items of type {expected_type}, not {type(arg)}')

    def _non_negative(self, arg: int | float, arg_name: str):
        if arg < 0:
            raise ValueError(f'Argument \'{arg_name}\' cannot be negative')
        
    def _positive(self, arg: int | float, arg_name: str):
        if not arg > 0:
            raise ValueError(f'Argument \'{arg_name}\' must be positive')
        
    def _upper_bound(self, arg: int | float, arg_name: str, upper_bound: int | float):
        if arg > upper_bound:
            raise ValueError(f'Argument \'{arg_name}\' cannot be larger than {upper_bound}')
        
    def _exists_in_dict(self, arg: Any, arg_name: str, container: dict):
        if arg not in container:
            raise ValueError(f'Argument \'{arg_name}\' does not exist in dict')


    class Analysis:
        def __init__(self) -> None:
            self._validation = Validation()
        
        def constructor_arguments(self, net: Network, generate_forests: bool, min_edges: int, timeout: int, delay_unit: DisplayUnit, runtime_unit: DisplayUnit, temp_folder: str, results_folder: str, verbose: List[VerboseKW]) -> None:
            self._validation._type(net, 'net', Network)
            self._validation._type(generate_forests, 'generate_forests', bool)
            self._validation._type(min_edges, 'min_edges', int)
            self._validation._type(timeout, 'timeout', int)
            self._validation._type(delay_unit, 'delay_unit', DisplayUnit)
            self._validation._type(runtime_unit, 'runtime_unit', DisplayUnit)
            self._validation._type(temp_folder, 'temp_folder', str)
            self._validation._type(results_folder, 'results_folder', str)
            self._validation._type(verbose, 'verbose', list)
            self._validation._non_negative(min_edges, 'min_edges')
            self._validation._positive(timeout, 'timeout')
            self._validation._types_in_list(verbose, 'verbose', VerboseKW)

        def callable(self, generate_forests: bool, foo: Callable) -> None:
            if not generate_forests:
                raise ValueError(f'Cannot execute function \'{foo.__name__}\' because generate_forests option was set to False in the constructor')

        def foi(self, foi: int, num_flows: int) -> None:
            self._validation._type(foi, 'foi', int)
            self._validation._non_negative(foi, 'foi')
            self._validation._upper_bound(foi, 'foi', num_flows-1)

        def forest(self, forest: List[Tuple[int, int]], edges: List[Tuple[int, int]]) -> None:
            self._validation._type(forest, 'forest', list)
            for edge in forest:
                if len(edge) != 2:
                    raise ValueError(f'Edges within \'forest\' must be of length 2, not {len(edge)}')
                if not isinstance(edge[0], int) or not isinstance(edge[1], int):
                    raise TypeError(f'Vertex descriptors within edges within \'forest\' must be of type {int}')
                if edge not in edges:
                    raise ValueError(f'Edges within \'forest\' must be valid edges of this network')

        def index(self, index: int, forests: List[List[Tuple[int, int]]]) -> None:
            self._validation._type(index, 'index', int)
            self._validation._non_negative(index, 'index')            
            self._validation._upper_bound(index, 'index', len(forests)-1)            
            
        def indexes(self, indexes: List[int]) -> None:
            self._validation._type(indexes, 'indexes', list)
            
        def filename(self, filename: str) -> None:
            self._validation._type(filename, 'filename', str)
            
            
    class Stats:
        def __init__(self) -> None:
            self._validation = Validation()
        
        def constructor_arguments(self, results_folder: str, filename: str) -> None:
            self._validation._type(results_folder, 'results_folder', str)
            self._validation._type(filename, 'filename', str)

        def foi(self, foi: int, results: dict) -> None:
            self._validation._type(foi, 'foi', int)
            self._validation._non_negative(foi, 'foi')
            self._validation._exists_in_dict(foi, 'foi', results)
            

    class Networks:
        def __init__(self) -> None:
            self._validation = Validation()