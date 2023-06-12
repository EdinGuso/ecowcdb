# Standard Library Imports
from itertools import combinations
from math import ceil, comb
from random import randint, sample, seed
from typing import List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import ForestGeneration

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.curves import RateLatency, TokenBucket
from ecowcdb.panco.descriptor.flow import Flow
from ecowcdb.panco.descriptor.network import Network, dfs
from ecowcdb.panco.descriptor.server import Server



# returns whether a given network is a forest
def is_forest(net: Network) -> bool:

    for i in range(net.num_servers):
        if len(net.successors[i]) > 1:
            return False
    
    try:
        for i in range(net.num_servers):
            dfs(i, net.num_servers, net.successors, net.num_servers * [0], [], [])
    except NameError as e:
        if e.args[0] == 'Network has cycles: feed-forward analysis impossible':
            return False
        raise e

    return True

# returns a list of all possible lists of edges that are forests
def __all_forests(net: Network, min_edges: int) -> List[List[Tuple[int, int]]]:

    subsets = []
    edges = list(net.edges.keys())

    for i in range(min_edges, len(edges) + 1):
        for subset in combinations(edges, i):
            if is_forest(net.decomposition(list(subset))[0]):
                subsets.append(list(subset))

    return subsets

# returns a list of subset of all possible lists of edges that are forests 
def __subset_forests(net: Network, min_edges: int, num_forests: int) -> List[List[Tuple[int, int]]]:

    if num_forests == 0:
        return []
    
    FAIL_LIMIT = 1000

    seed(0)
    subsets = [[]]
    edges = list(net.edges.keys())

    consecutive_fail = 0
    while len(subsets) < num_forests:
        num_edges = randint(min_edges,len(edges))
        subset = sorted(sample(edges, num_edges), key=lambda x: x[0])
        if subset not in subsets and is_forest(net.decomposition(subset)[0]):
            subsets.append(subset)
            consecutive_fail = 0
        else:
            consecutive_fail += 1

        if consecutive_fail > FAIL_LIMIT:
            raise ValueError(f'Argument \'num_forests\' exceedes the number of valid forests')

    return sorted(subsets, key=lambda x: len(x))
    # return subsets

def generate_forests(net: Network, forest_generation: ForestGeneration, min_edges: int, num_forests: int) -> List[List[Tuple[int, int]]]:
    match forest_generation:
        case ForestGeneration.Empty:
            return []
        case ForestGeneration.Partial:
            return __subset_forests(net, min_edges, num_forests)
        case ForestGeneration.All:
            return __all_forests(net, min_edges)
        case _:
            raise ValueError(f'Unhandled forest generation type: {generate_forests}')
    

    

# scales everything other than latency, does not change the output unit
def scale_network(net: Network, factor: float) -> Network:

    if factor == 1.0:
        return net

    servers = []
    for server in net.servers:

        service_curves = []
        for service_curve in server.service_curve:
            service_curves.append(RateLatency(service_curve.rate * factor, service_curve.latency))

        shapers = []
        for shaper in server.max_service_curve:
            shapers.append(TokenBucket(shaper.sigma * factor, shaper.rho * factor))

        servers.append(Server(service_curves, shapers))

    flows = []
    for flow in net.flows:
        
        arrival_curves = []
        for arrival_curve in flow.arrival_curve:
            arrival_curves.append(TokenBucket(arrival_curve.sigma * factor, arrival_curve.rho * factor))

        flows.append(Flow(arrival_curves, flow.path))

    return Network(servers, flows)

def generate_symmetric_forests(forest: List[Tuple[int, int]], N: int) -> List[List[Tuple[int, int]]]:
    symmetric_forests = [set(forest)]

    for i in range(1,N):
        symmetric_forest = set()
        for edge in forest:
            symmetric_forest.add(((edge[0]+i)%N,(edge[1]+i)%N))
        if symmetric_forest in symmetric_forests:
            break
        symmetric_forests.append(symmetric_forest)
    
    return [sorted(list(x), key=lambda x: x[0]) for x in symmetric_forests]
