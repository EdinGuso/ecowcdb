"""
 File containing the tool for simple statistical analysis.
"""

# Standard Library Imports
from pickle import load
from typing import Dict, List, Tuple

# Third-Party Library Imports
from scipy.stats import pearsonr

# Local Imports - utility libraries
from ecowcdb.util.validation import Validation



class Stats:
    """
     desc.

     Attributes:
         __validation (Validation.Stats, private): Validation object used to validate user inputs.
         __RAW_FILE_FORMAT (str, private): File extension of the raw dump of the results.
         __results (Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]], private): Dictionary which holds the
         computed results.

     Methods:
         delay_runtime_correlation (public): Print the correlation between delays and runtimes.
         forestsize_delay_correlation (public): Print the correlation between forest sizes and delays.
         forestsize_runtime_correlation (public): Print the correlation between forest sizes and runtimes.
    """
    __validation: Validation.Stats
    __RAW_FILE_FORMAT: str
    __results: Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]]

    def __init__(self, results_folder: str, filename: str) -> None:
        """
         Initialize the object by loading the file. The file is expected to containt results obtained by the Analysis
         object.
         
         Args:
         	 results_folder (str, required): Folder in which analysis results are stored. It is the user's
             responsibility to ensure that the provided folder exists.
         	 filename (str, required): Name of the file to load. The name should not include the extension as the
             extension is added automatically within the function. It is user's responsibility to ensure that the given
             file exists.
        """
        self.__validation = Validation.Stats()
        self.__validation.constructor_arguments(results_folder, filename)
        self.__RAW_FILE_FORMAT = '.pickle'

        filepath = results_folder + filename + self.__RAW_FILE_FORMAT
        with open(filepath, 'rb') as file:
            loaded_object = load(file)
            self.__results = loaded_object['results']

    def delay_runtime_correlation(self, foi: int) -> None:
        """
         Calculate and print the Pearson correlation between delays and runtimes.
         
         Args:
         	 foi (int, required): Flow of interest.
        """
        self.__validation.foi(foi, self.__results)

        delays = [item[1] for item in self.__results[foi]]
        runtimes = [item[2] for item in self.__results[foi]]

        correlation, p_value = pearsonr(delays, runtimes)
        print(f'The correlation between delays and runtimes:\n{correlation=}\n{p_value=}')

    def forestsize_delay_correlation(self, foi: int) -> None:
        """
         Calculate and print the Pearson correlation between forest sizes and delays.
         
         Args:
         	 foi (int, required): Flow of interest.
        """
        self.__validation.foi(foi, self.__results)

        forest_sizes = [len(item[0]) for item in self.__results[foi]]
        delays = [item[1] for item in self.__results[foi]]

        correlation, p_value = pearsonr(forest_sizes, delays)
        print(f'The correlation between forest sizes and delays:\n{correlation=}\n{p_value=}')

    def forestsize_runtime_correlation(self, foi: int) -> None:
        """
         Calculate and print the Pearson correlation between forest sizes and runtimes.
         
         Args:
         	 foi (int, required): Flow of interest.
        """
        self.__validation.foi(foi, self.__results)

        forest_sizes = [len(item[0]) for item in self.__results[foi]]
        runtimes = [item[2] for item in self.__results[foi]]

        correlation, p_value = pearsonr(forest_sizes, runtimes)
        print(f'The correlation between forest sizes and runtimes:\n{correlation=}\n{p_value=}')
