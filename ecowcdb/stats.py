"""
 File containing the tool for simple statistical analysis.
"""

# Standard Library Imports
from pickle import load
from statistics import median
from typing import Dict, List, Tuple

# Third-Party Library Imports
from scipy.stats import pearsonr

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.network import Network

# Local Imports - utility libraries
from ecowcdb.util.network import flow_preserving_min_depth_max_forest
from ecowcdb.util.validation import Validation



class Stats:
    """
     desc.

     Attributes:
         __validation (Validation.Stats, private): Validation object used to validate user inputs.
         __RAW_FILE_FORMAT (str, private): File extension of the raw dump of the results.
         __net (Network, private): Network object for which the analysis will be performed.
         __results (Dict[int, List[Tuple[List[Tuple[int, int]], float, float]]], private): Dictionary which holds the
         computed results.

     Methods:
         delay_runtime_correlation (public): Print the correlation between delays and runtimes.
         forestsize_delay_correlation (public): Print the correlation between forest sizes and delays.
         forestsize_runtime_correlation (public): Print the correlation between forest sizes and runtimes.
         __forest_ranking (private): Computes and prints the forest's ranking among all other forests.
         best_forest_ranking (public): Computes and prints the best forest's ranking among all other forests.
         forest_ranking (public): Computes and prints the forest's ranking among all other forests.
         quick_forest_ranking (public): Computes and prints the quick forest's ranking among all other forests.

    """
    __validation: Validation.Stats
    __RAW_FILE_FORMAT: str
    __net: Network
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
            self.__net = loaded_object['net']
            self.__results = loaded_object['results']

    def __filter_inf(self, list1: List[float], list2: List[float]) -> Tuple[List[float], List[float]]:
        """
         Filters inf values from two lists. If any list has an inf value at any index, items from both lists are
         removed. This is a helper function for correlation functions.
         
         Args:
         	 list1 (List[float], required): List of float values to be filtered
         	 list2 (List[float], required): List of float values to be filtered ( same order as list1 )
         
         Returns: 
         	 Tuple[List[float], List[float]]: A tuple of two lists with filtered inf values from each list
        """
        filtered_list1 = []
        filtered_list2 = []
        for item1, item2 in zip(list1, list2):
            if item1 != float('inf') and item2 != float('inf'):
                filtered_list1.append(item1)
                filtered_list2.append(item2)

        return filtered_list1, filtered_list2

    def delay_runtime_correlation(self, foi: int) -> None:
        """
         Calculate and print the Pearson correlation between delays and runtimes.
         
         Args:
         	 foi (int, required): Flow of interest.
        """
        self.__validation.foi(foi, self.__results)

        delays = [item[1] for item in self.__results[foi]]
        runtimes = [item[2] for item in self.__results[foi]]

        delays, runtimes = self.__filter_inf(delays, runtimes)

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

        forest_sizes, delays = self.__filter_inf(forest_sizes, delays)

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

        forest_sizes, runtimes = self.__filter_inf(forest_sizes, runtimes)

        correlation, p_value = pearsonr(forest_sizes, runtimes)
        print(f'The correlation between forest sizes and runtimes:\n{correlation=}\n{p_value=}')

    def __forest_ranking(self, foi: int, forest: List[Tuple[int, int]]) -> None:
        """
         Computes and prints the forest's ranking among all other forests. Helper function for *forest_ranking.
         
         Args:
         	 foi (int, required): Flow of interest.
         	 forest (List[Tuple[int, int]], required): Forest to rank. This is a list of edges.
        """
        results = self.__results[foi]
        delay_ordered_forests = [result[0] for result in results]
        forest_index = delay_ordered_forests.index(forest)
        median_runtime = median([result[2] for result in results])

        top = (forest_index+1)/len(results)
        print(f'The forest is in the top {100*top:.2f}% in delay.')

        comp_median = results[forest_index][2] / median_runtime
        if comp_median > 1:
            print(f'The forest\'s runtime is {100*(comp_median-1):.2f}% higher than the median runtime.')
        else:
            print(f'The forest\'s runtime is {100*(1-comp_median):.2f}% lower than the median runtime.')

    def best_forest_ranking(self, foi: int) -> None:
        """
         Computes and prints the best forest's ranking among all other forests.
         
         Args:
         	 foi (int, required): Flow of interest.
        """
        self.__validation.foi(foi, self.__results)
        
        best_forest = flow_preserving_min_depth_max_forest(list(self.__net.edges.keys()), self.__net.num_servers,
                                                           self.__net.flows[foi].path)
        self.__forest_ranking(foi, best_forest)

    def forest_ranking(self, foi: int, max_depth: int) -> None:
        """
         Computes and prints the forest's ranking among all other forests.
         
         Args:
         	 foi (int, required): Flow of interest.
             max_depth (int, required): Max depth used in heuristic forest generation.
        """
        self.__validation.foi(foi, self.__results)
        self.__validation.max_depth(max_depth)

        forest = flow_preserving_min_depth_max_forest(list(self.__net.edges.keys()), self.__net.num_servers,
                                                      self.__net.flows[foi].path, max_depth)
        self.__forest_ranking(foi, forest)

    def quick_forest_ranking(self, foi: int, max_depth: int) -> None:
        """
         Computes and prints the quick forest's ranking among all other forests.
         
         Args:
         	 foi (int, required): Flow of interest.
             max_depth (int, required): Max depth used in heuristic forest generation.
        """
        self.__validation.foi(foi, self.__results)
        self.__validation.max_depth(max_depth)

        quick_forest = flow_preserving_min_depth_max_forest(list(self.__net.edges.keys()), self.__net.num_servers,
                                                            self.__net.flows[foi].path, max_depth, True)
        self.__forest_ranking(foi, quick_forest)
