"""
 desc.
"""

# Standard Library Imports
from pickle import load
from typing import Dict, List, Tuple

# Third-Party Library Imports
from scipy.stats import pearsonr

# Local Imports - utility libraries
from ecowcdb.util.validation import Validation



class Stats:
    __validation: Validation.Stats
    __RAW_FILE_FORMAT: str
    __results: Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]]

    def __init__(self, results_folder: str, filename: str) -> None:
        self.__validation = Validation.Stats()
        self.__validation.constructor_arguments(results_folder, filename)
        self.__RAW_FILE_FORMAT = '.pickle'

        filepath = results_folder + filename + self.__RAW_FILE_FORMAT
        with open(filepath, 'rb') as file:
            self.__results = load(file)

    def delay_runtime_correlation(self, foi: int) -> None:
        self.__validation.foi(foi, self.__results)

        delays = [item[1] for item in self.__results[foi]]
        runtimes = [item[2] for item in self.__results[foi]]

        correlation, p_value = pearsonr(delays, runtimes)
        print(f'The correlation between delays and runtimes:\n{correlation=}\n{p_value=}')

    def forestsize_delay_correlation(self, foi: int) -> None:
        self.__validation.foi(foi, self.__results)

        forest_sizes = [len(item[0]) for item in self.__results[foi]]
        delays = [item[1] for item in self.__results[foi]]

        correlation, p_value = pearsonr(forest_sizes, delays)
        print(f'The correlation between forest sizes and delays:\n{correlation=}\n{p_value=}')

    def forestsize_runtime_correlation(self, foi: int) -> None:
        self.__validation.foi(foi, self.__results)

        forest_sizes = [len(item[0]) for item in self.__results[foi]]
        runtimes = [item[2] for item in self.__results[foi]]

        correlation, p_value = pearsonr(forest_sizes, runtimes)
        print(f'The correlation between forest sizes and runtimes:\n{correlation=}\n{p_value=}')
