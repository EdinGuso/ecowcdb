# Local Imports - ecowcdb libraries
from ecowcdb.ecowcdb import ECOWCDB
from ecowcdb.networks import Networks
from ecowcdb.options import NetworkType



def main():
    R = 10**7 # Kb/s
    L = 10**-5 # s
    S = 8 # Kb
    N = 12 # servers
    load = 0.5
    
    net = Networks.Ring().full(R, L, S, N, load, NetworkType.Symmetric)
    ecowcdb = ECOWCDB(net, 'temp/')
    
    flow_of_interest = 0

    delay_a, _ = ecowcdb.algorithm_a(flow_of_interest)
    delay_b, _ = ecowcdb.algorithm_b(flow_of_interest, max_depth=5)
    delay_c, _ = ecowcdb.algorithm_c(flow_of_interest, max_depth=5)

    print(f'{delay_a=}s')
    print(f'{delay_b=}s')
    print(f'{delay_c=}s')


if __name__ == '__main__':
    main()
