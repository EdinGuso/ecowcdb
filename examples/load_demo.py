# Local Imports - ecowcdb libraries
from ecowcdb.analysis import Analysis
from ecowcdb.networks import Networks
from ecowcdb.options import DisplayUnit, ForestGeneration, NetworkType



def main():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 5 # servers
    load = 0.5
    
    net = Networks.Ring().complete_semi(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(
        net,
        forest_generation=ForestGeneration.Empty,
        delay_unit=DisplayUnit.MicroSecond,
        runtime_unit=DisplayUnit.Second,
        results_folder='results/'
        )
    
    flow_of_interest = 0

    filename = 'demo1'
    analysis.load_raw_results(filename)

    analysis.display_results(flow_of_interest)


if __name__ == '__main__':
    main()
