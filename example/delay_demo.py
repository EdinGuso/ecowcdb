# Local Imports - ecowcdb libraries
from ecowcdb.analysis import Analysis
from ecowcdb.networks import Networks
from ecowcdb.options import ForestGeneration, NetworkType, VerboseKW



def main():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 12 # servers
    load = 0.5
    
    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    analysis = Analysis(
        net,
        forest_generation=ForestGeneration.Empty,
        timeout=60,
        temp_folder='temp/',
        verbose=[
            VerboseKW.Network,
            VerboseKW.LP_Errors
            ]
        )
    
    flow_of_interest = 0
    forest = [(0, 1), (1, 2), (2, 3), (10, 11), (11, 0)]

    delay = analysis.delay(flow_of_interest, forest)
    print(f'{delay=}s')


if __name__ == '__main__':
    main()
