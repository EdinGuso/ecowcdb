# Local Imports - ecowcdb libraries
from ecowcdb.analysis import Analysis
from ecowcdb.networks import Networks
from ecowcdb.options import DisplayUnit, ForestGeneration, NetworkType, VerboseKW



def main():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 5 # servers
    load = 0.5
    
    net = Networks.Ring().complete_semi(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(
        net,
        forest_generation=ForestGeneration.Partial,
        num_forests=10,
        min_edges=0,
        timeout=1800,
        delay_unit=DisplayUnit.MicroSecond,
        runtime_unit=DisplayUnit.Second,
        temp_folder='temp/',
        results_folder='results/',
        verbose=[
            VerboseKW.ES_ProgressBar,
            VerboseKW.FG_ProgressBar,
            VerboseKW.LP_Errors
            ]
        )
    
    flow_of_interest = 0

    analysis.exhaustive_search(flow_of_interest)

    filename = 'demo2'
    analysis.save_results(flow_of_interest, filename)
    analysis.save_raw_results(filename)

    analysis.display_results(0)


if __name__ == '__main__':
    main()
