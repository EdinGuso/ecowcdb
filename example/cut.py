# add directories to path so that ecowcdb and panco are importable
import sys
import os.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../")))



# Local Imports - ecowcdb libraries
from ecowcdb.analysis import Analysis
from ecowcdb.networks import Networks
from ecowcdb.options import DisplayUnit, ForestGeneration, NetworkType, VerboseKW
from ecowcdb.stats import Stats



def delay_by_index_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 8 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, timeout=30, temp_folder='../temp/',
                        verbose=[VerboseKW.Forest, VerboseKW.LPErrorMsg])
    delay = analysis.delay_by_index(0, 252)
    print(f'{delay=}')



def delay_by_forest_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 12 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, timeout=600, generate_forests=False,
                        temp_folder='../temp/', verbose=[VerboseKW.LPErrorMsg, VerboseKW.LPProgress])
    delay = analysis.delay(0, [(0, 1), (1, 2), (2, 3), (10, 11), (11, 0)])
    print(f'{delay=}')



def quick_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 3 # servers
    load = 0.9

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.AsymmetricFlow)
    analysis = Analysis(net, min_edges=0, timeout=10,
                        delay_unit=DisplayUnit.MicroSecond,
                        runtime_unit=DisplayUnit.MilliSecond,
                        temp_folder='../temp/',
                        verbose=[VerboseKW.Network, VerboseKW.LPErrorMsg, VerboseKW.ProgressBar])
    analysis.exhaustive_search(0)
    analysis.display_results(0)



def large_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 11 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, min_edges=0, timeout=600,
                        delay_unit=DisplayUnit.MilliSecond,
                        runtime_unit=DisplayUnit.Second,
                        temp_folder='../temp/', results_folder='../results/',
                        verbose=[VerboseKW.LPErrorMsg, VerboseKW.ProgressBar])
    analysis.exhaustive_search(0)
    analysis.save_results(0, 'large_full_ring_11')
    analysis.save_raw_results('large_full_ring_11')
    analysis.display_results(0)



def partial_demo():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 24 # servers
    load = 0.5

    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    # net = Networks.Mesh().simple(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(net, forest_generation=ForestGeneration.Partial, num_forests=50, timeout=7200,
                        delay_unit=DisplayUnit.MicroSecond, runtime_unit=DisplayUnit.Minute,
                        temp_folder='../temp/', results_folder='../results/',
                        verbose=[VerboseKW.LPErrorMsg, VerboseKW.ProgressBar])
    analysis.exhaustive_search(0)
    analysis.save_results(0, 'partial_full_ring_20')
    analysis.save_raw_results('partial_full_ring_20')
    analysis.display_results(0)



def load_demo():
    net = Networks().empty()
    analysis = Analysis(net, generate_forests=False, results_folder='../results/', delay_unit=DisplayUnit.MilliSecond)
    analysis.load_raw_results('large_full_ring_12')
    analysis.display_results(0)



def stat_demo():
    stats = Stats('../results/', 'large_full_ring_11')
    stats.pearson_correlation(0)



if __name__ == '__main__':
    # delay_by_index_demo()
    # delay_by_forest_demo()
    # quick_demo()
    # large_demo()
    partial_demo()
    # load_demo()
    # stat_demo()