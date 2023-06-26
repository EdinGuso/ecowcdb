# Local Imports - ecowcdb libraries
from ecowcdb.ecowcdb import ECOWCDB
from ecowcdb.networks import Networks
from ecowcdb.options import NetworkType



def main():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 24 # servers
    load = 0.5
    
    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    ecowcdb = ECOWCDB(net, 'temp/')
    
    flow_of_interest = 0

    best_delay = ecowcdb.delay(flow_of_interest)
    worse_delay = ecowcdb.delay(flow_of_interest, max_depth=5)

    print(f'{best_delay=}s')
    print(f'{worse_delay=}s')


if __name__ == '__main__':
    main()
