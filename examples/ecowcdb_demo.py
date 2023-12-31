# Local Imports - ecowcdb libraries
from ecowcdb.ecowcdb import ECOWCDB
from ecowcdb.networks import Networks
from ecowcdb.options import NetworkType



def main():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 5 # servers
    load = 0.5
    
    net = Networks.Ring().complete_semi(R, L, S, N, load, NetworkType.Symmetric)
    ecowcdb = ECOWCDB(net, 'temp/')
    
    flow_of_interest = 0

    delay_a, _ = ecowcdb.min_cut_forest(flow_of_interest)
    delay_b, _ = ecowcdb.min_cut_forest_with_restricted_depth(flow_of_interest, max_depth=2)
    delay_c, _ = ecowcdb.min_cut_tree_with_restricted_depth(flow_of_interest, max_depth=2)

    print(f'{delay_a=}s')
    print(f'{delay_b=}s')
    print(f'{delay_c=}s')


if __name__ == '__main__':
    main()
