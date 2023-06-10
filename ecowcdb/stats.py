# Standard Library Imports
from pickle import load

# Third-Party Library Imports
from scipy.stats import pearsonr

# Local Imports - utility libraries
from ecowcdb.util.validation import Validation



class Stats:
    def __init__(self, results_folder: str, filename: str) -> None:
        self._validaton = Validation.Stats()
        self._validaton.constructor_arguments(results_folder, filename)
        self._RAW_FILE_FORMAT = '.pickle'

        filepath = results_folder + filename + self._RAW_FILE_FORMAT
        with open(filepath, 'rb') as file:
            self._results = load(file)

    def pearson_correlation(self, foi: int) -> None:
        self._validaton.foi(foi, self._results)

        delays = [item[1] for item in self._results[foi]]
        runtimes = [item[2] for item in self._results[foi]]

        correlation, p_value = pearsonr(delays, runtimes)
        print(f'The correlation between delays and runtimes:\n{correlation=}\n{p_value=}')
