# add directories to path so that ecowcdb and panco are importable
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))



# Local Imports - ecowcdb libraries
from ecowcdb.analysis import Analysis
from ecowcdb.ecowcdb import ECOWCDB
from ecowcdb.networks import Networks
from ecowcdb.options import DisplayUnit, ForestGeneration, NetworkType, VerboseKW
from ecowcdb.stats import Stats



def exhaustive_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 4 # servers
    load = 0.5
    
    net = Networks.Mesh().simple(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, forest_generation=ForestGeneration.All, min_edges=0, timeout=600,
                        delay_unit=DisplayUnit.MicroSecond, runtime_unit=DisplayUnit.Second,
                        temp_folder='../temp/', results_folder='../results/',
                        verbose=[VerboseKW.ES_ProgressBar, VerboseKW.LP_Errors])
    analysis.exhaustive_search(0)
    analysis.save_results(0, f'mesh/simple/exhaustive_{N}')
    analysis.save_raw_results(f'mesh/simple/exhaustive_{N}')
    analysis.display_results(0)


def partial_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 32 # servers
    load = 0.5

    net = Networks.Tandem().source_sink(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, forest_generation=ForestGeneration.Partial, num_forests=100, min_edges=0, timeout=1800,
                        delay_unit=DisplayUnit.MicroSecond, runtime_unit=DisplayUnit.Minute,
                        temp_folder='../temp/', results_folder='../results/',
                        verbose=[VerboseKW.ES_ProgressBar, VerboseKW.LP_Errors])
    analysis.exhaustive_search(0)
    analysis.save_results(0, f'tandem/source_sink/partial_{N}')
    analysis.save_raw_results(f'tandem/source_sink/partial_{N}')
    analysis.display_results(0)


def quick_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 3 # servers
    load = 0.9

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.AsymmetricFlow)
    analysis = Analysis(net, timeout=10, delay_unit=DisplayUnit.MicroSecond,
                        runtime_unit=DisplayUnit.MilliSecond, temp_folder='../temp/',
                        verbose=[VerboseKW.Network, VerboseKW.LP_Errors, VerboseKW.ES_ProgressBar])
    analysis.exhaustive_search(0)
    analysis.display_results(0)


def load_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 24 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, forest_generation=ForestGeneration.Empty, results_folder='../results/', delay_unit=DisplayUnit.MicroSecond)
    analysis.load_raw_results('partial_full_ring_24')
    analysis.display_results(0)


def delay_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 12 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, forest_generation=ForestGeneration.Empty, timeout=60,
                        temp_folder='../temp/', verbose=[VerboseKW.Network, VerboseKW.LP_Errors])
    delay = 10**6 * analysis.delay(0, [(0, 1), (1, 2), (2, 3), (10, 11), (11, 0)])
    print(f'{delay=} microseconds')


def stat_demo():
    stats = Stats('../results/', 'tandem/sink_tree/exhaustive_12')
    stats.delay_runtime_correlation(0)
    stats.forestsize_delay_correlation(0)
    stats.forestsize_runtime_correlation(0)


def ecowcdb_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 12 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    ecowcdb = ECOWCDB(net, '../temp/')
    delay = ecowcdb.delay(0, 120)

    print(f'ECOWCDB returned {delay=}')


if __name__ == '__main__':
    # exhaustive_demo()
    # partial_demo()
    # quick_demo()
    # load_demo()
    # delay_demo()
    # stat_demo()
    ecowcdb_demo()
