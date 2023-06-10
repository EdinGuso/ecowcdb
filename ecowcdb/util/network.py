# Standard Library Imports
from itertools import combinations
from typing import List, Tuple

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.curves import RateLatency, TokenBucket
from ecowcdb.panco.descriptor.flow import Flow
from ecowcdb.panco.descriptor.network import Network, dfs
from ecowcdb.panco.descriptor.server import Server



# returns whether a given network is a forest
def __is_forest(net: Network) -> bool:

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
def all_forests(net: Network, min_edges: int) -> List[List[Tuple[int, int]]]:

    subsets = []
    edges = list(net.edges.keys())

    for i in range(min_edges, len(edges) + 1):
        for subset in combinations(edges, i):
            if __is_forest(net.decomposition(list(subset))[0]):
                subsets.append(list(subset))

    return subsets

# scales everything other than latency, does not change the output unit
def scale_network(net: Network, factor: float) -> Network:

    if factor == 1:
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