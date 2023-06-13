# Standard Library Imports
from itertools import combinations
from random import randint, sample, seed
from typing import List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import ForestGeneration

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.curves import RateLatency, TokenBucket
from ecowcdb.panco.descriptor.flow import Flow
from ecowcdb.panco.descriptor.network import Network, dfs
from ecowcdb.panco.descriptor.server import Server



def __all_forests(net: Network, min_edges: int) -> List[List[Tuple[int, int]]]:
    """
     Returns all valid forests for the given network.
     This is a helper function for generate_forests.
     
     Args:
     	 net (Network, required): Network to generate forests for.
     	 min_edges (int, required): Minimum number of edges that should be included in the forest.
     
     Returns: 
     	 List[List[Tuple[int, int]]]: List of forests, where each forest is a list of edge tuples.
    """
    forests = []
    edges = list(net.edges.keys())
    for i in range(min_edges, len(edges)+1):
        for subset_edges in combinations(edges, i):
            if is_forest(net.decomposition(list(subset_edges))[0]):
                forests.append(list(subset_edges))
    
    return forests

def __subset_forests(net: Network, min_edges: int, num_forests: int)-> List[List[Tuple[int, int]]]:
    """
     Returns a random subset of valid forests for the given network.
     This is a helper function for generate_forests.
     
     Args:
     	 net (Network, required): Network to generate forests for.
     	 min_edges (int, required): Minimum number of edges that should be included in the forest.
     	 num_forests (int, required): The number of forests to be returned.
          
     Raises:
         ValueError: If sampling a random forest fails too many times consecutively.
         This may give false positives.
     
     Returns: 
     	 List[List[Tuple[int, int]]]: List of forests, where each forest is a list of edge tuples.
    """
    if num_forests == 0:
        return []
    
    FAIL_LIMIT = 10**4
    seed(0)
    forests = [[]]
    edges = list(net.edges.keys())
    consecutive_fails = 0
    # Randomly sample the forests and add them to the list of valid forests.
    while len(forests) < num_forests:
        num_edges = randint(min_edges,len(edges))
        subset_edges = sorted(sample(edges, num_edges), key=lambda x: x[0])
        if subset_edges not in forests and is_forest(net.decomposition(subset_edges)[0]):
            forests.append(subset_edges)
            consecutive_fails = 0
        else:
            consecutive_fails += 1
            if consecutive_fails > FAIL_LIMIT:
                raise ValueError(f'Argument \'num_forests\' exceedes the number of valid forests')

    # Sort the forests based on the length. Smaller forests will be processed first.
    return sorted(forests, key=lambda x: len(x))

def is_forest(net: Network) -> bool:
    """
     Check if a network is a forest.
     A network is a forest if all the servers have at most 1 successor and there are no cycles.
     
     Args:
     	 net (Network, required): Network to be checked.
          
     Raises:
         NameError: Propagates all the unexpected NameErrors from dfs function.
     
     Returns: 
     	 bool: True if the network is a forest False otherwise.
               Note that this does not check if the network is connected.
    """
    N = net.num_servers
    for i in range(N):
        if len(net.successors[i]) > 1:
            return False
    
    try:
        for i in range(N):
            dfs(i, N, net.successors, N * [0], [], [])
    except NameError as e:
        if e.args[0] == 'Network has cycles: feed-forward analysis impossible':
            return False
        raise e

    return True

def generate_forests(net: Network, forest_generation: ForestGeneration, min_edges: int, num_forests: int
                     ) -> List[List[Tuple[int, int]]]:
    """
     Generate forests based on the network.
     Returns no forests if ForestGeneration.Empty.
     Returns a random subset of valid forests if ForestGeneration.Partial.
     Returns all valid forests if ForestGeneration.All.
     
     Args:
         net (Network, required): Network to generate forests for.
         forest_generation (ForestGeneration, required): The type of forest generation.
     	 min_edges (int, required): Minimum number of edges that should be included in the forest.
     	 num_forests (int, required): The number of forests to be returned.
          
     Raises:
         ValueError: If an unexpected forest generation option is received.
     
     Returns: 
     	 List[List[Tuple[int, int]]]: List of forests, where each forest is a list of edge tuples.
    """
    match forest_generation:
        case ForestGeneration.Empty:
            return []
        case ForestGeneration.Partial:
            return __subset_forests(net, min_edges, num_forests)
        case ForestGeneration.All:
            return __all_forests(net, min_edges)
        case _:
            raise ValueError(f'Unhandled forest generation type: {generate_forests}')

def generate_symmetric_forests(forest: List[Tuple[int, int]], N: int) -> List[List[Tuple[int, int]]]:
    """
     Generates symmetric forests by orienting the given forest around.
     This function only works for cycle networks with symmetric servers and flows.
     
     Args:
     	 forest (List[Tuple[int, int]], required): A list of edge tuples
     	 N (int, required): The number of servers in the network
     
     Returns: 
     	 List[List[Tuple[int, int]]]: A list of symmetrically oriented forests.
    """
    symmetric_forests = [set(forest)]
    for i in range(1,N):
        symmetric_forest = set()
        for edge in forest:
            symmetric_forest.add(((edge[0]+i)%N,(edge[1]+i)%N))
        # Some forests do not have N unique orientations
        if symmetric_forest in symmetric_forests:
            break
        symmetric_forests.append(symmetric_forest)
    
    return [sorted(list(x), key=lambda x: x[0]) for x in symmetric_forests]

def scale_network(net: Network, factor: float) -> Network:
    """
     Multiples all rate and burst values in the network by the factor. Latency values are unchanged.
     This function is called if lp_solve struggles to solve the lp.
     
     Args:
     	 net (Network, required): The network to scale.
     	 factor (float, required): The factor by which to scale the network.
     
     Returns: 
     	 Network: A copy of the network scaled by the factor.
    """
    # Returns back the network if factor is 1.0
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
