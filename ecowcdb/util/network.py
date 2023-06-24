"""
 File containing the network and forest related utility functions.
"""

# Standard Library Imports
from itertools import combinations
from math import comb
from random import randint, sample, seed
from typing import List, Tuple

# Third-Party Library Imports
from tqdm import tqdm

# Local Imports - ecowcdb libraries
from ecowcdb.options import ForestGeneration

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.curves import RateLatency, TokenBucket
from ecowcdb.panco.descriptor.flow import Flow
from ecowcdb.panco.descriptor.network import Network, dfs
from ecowcdb.panco.descriptor.server import Server



def __all_forests(net: Network, min_edges: int, verbose: bool) -> List[List[Tuple[int, int]]]:
    """
     Returns all valid forests for the given network. This is a helper function for generate_forests.
     
     Args:
     	 net (Network, required): Network to generate forests for.
     	 min_edges (int, required): Minimum number of edges that should be included in the forest.
         verbose (bool, required): Whether the progressbar will be displayed or not
     
     Returns: 
     	 List[List[Tuple[int, int]]]: List of forests, where each forest is a list of edge tuples.
    """
    # Inner function defined to avoid code duplication.
    def loop():
        for i in range(min_edges, len(edges)+1):
            for subset_edges in combinations(edges, i):
                if is_forest(net.decomposition(list(subset_edges))[0]):
                    forests.append(list(subset_edges))
                if verbose:
                    pbar.update(1)

    forests = []
    edges = list(net.edges.keys())
    num_cuts = 2**len(edges)
    for i in range(0, min_edges):
        num_cuts -= comb(len(edges), i)
    
    if verbose:
        with tqdm(total=num_cuts, desc='Selecting all valid forests from all cuts', unit='cut') as pbar:
            loop()
    else:
        loop()
    
    return forests

def __subset_forests(net: Network, min_edges: int, num_forests: int, verbose: bool)-> List[List[Tuple[int, int]]]:
    """
     Returns a random subset of valid forests for the given network. This is a helper function for generate_forests.
     
     Args:
     	 net (Network, required): Network to generate forests for.
     	 min_edges (int, required): Minimum number of edges that should be included in the forest.
     	 num_forests (int, required): The number of forests to be returned.
         verbose (bool, required): Whether the progressbar will be displayed or not
          
     Raises:
         ValueError: If sampling a random forest fails too many times consecutively.
         This may give false positives.
     
     Returns: 
     	 List[List[Tuple[int, int]]]: List of forests, where each forest is a list of edge tuples.
    """
    # Inner function defined to avoid code duplication.
    def loop():
        FAIL_LIMIT = 10**4
        consecutive_fails = 0
        while len(forests) < num_forests:
            num_edges = randint(min_edges,len(edges))
            subset_edges = sorted(sample(edges, num_edges), key=lambda x: x[0])
            if subset_edges not in forests and is_forest(net.decomposition(subset_edges)[0]):
                forests.append(subset_edges)
                consecutive_fails = 0
                if verbose:
                    pbar.update(1)
            else:
                consecutive_fails += 1
                if consecutive_fails > FAIL_LIMIT:
                    raise ValueError(f'Argument \'num_forests\' exceedes the number of valid forests')

    if num_forests == 0:
        return []
    
    seed(0)
    edges = list(net.edges.keys())
    forests = [[]]
    if verbose:
        with tqdm(total=num_forests, desc='Selecting a subset of forests at random', unit='forest', initial=1) as pbar:
            loop()
    else:
        loop()

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

def generate_forests(net: Network, forest_generation: ForestGeneration, min_edges: int, num_forests: int, verbose: bool
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
            return __subset_forests(net, min_edges, num_forests, verbose)
        case ForestGeneration.All:
            return __all_forests(net, min_edges, verbose)
        case _:
            raise ValueError(f'Unhandled forest generation type: {forest_generation}')

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

def __path_to_edges(path: List[int]) -> List[Tuple[int, int]]:
    """
     Converts a path to a list of edges. This is a helper function for flow_preserving_min_depth_max_forest.
     
     Args:
     	 path (List[int], required): The path (list of servers) to convert to edges.
     
     Returns: 
     	 List[Tuple[int, int]]: The list of edges in the path.
    """
    edges = []
    for i in range(len(path)-1):
        edges.append((path[i], path[i+1]))
    return edges

def __edges_to_reverse_adj_list(edges: List[Tuple[int, int]], N: int) -> List[List[int]]:
    """
     Converts edges into a reverse adjacency list. This is a helper function for flow_preserving_min_depth_max_forest.
     
     Args:
     	 edges (List[Tuple[int, int]], required): List of edges.
     	 N (int, required): The number of servers in the network.
     
     Returns:
         List[List[int]]: The reverse adjacency list.
    """
    reverse_adj_list = [[] for _ in range(N)]
    for edge in edges:
        reverse_adj_list[edge[1]].append(edge[0])
    return reverse_adj_list

def flow_preserving_min_depth_max_forest(edges: List[Tuple[int, int]], N: int, flow_path: List[int],
                                         max_depth: int = -1) -> List[Tuple[int, int]]:
    """
     Computes the maximal forest with minimum depth while preserving (not cutting) the flow.
     
     Args:
     	 edges (List[Tuple[int, int]], required): List of edges.
     	 N (int, required): The number of servers in the network.
     	 flow_path (List[int], required): The flow path (list of servers).
     	 max_depth (int, optional): Maximum allowed depth of the forest. Negative values correspond to unlimited depth.
         If it is a non-negative value, flow preservation is not guaranteed. Defaults is -1 which means unlimited
         depth.
     
     Returns: 
     	 List[Tuple[int, int]]: The maximal forest.
    """
    reverse_adjacency_list = __edges_to_reverse_adj_list(edges, N)
    flow_edges = __path_to_edges(flow_path)
    forest = []
    visited = set()
    node_depth_list = []

    # First, add the edges along the flow to the forest.
    visited.add(flow_edges[-1][1])
    node_depth_list.append((flow_edges[-1][1], 0))
    for edge in flow_edges[::-1]:
        visited.add(edge[0])
        if node_depth_list[-1][1] == max_depth:
            node_depth_list.append((edge[0], 0))
        else:
            node_depth_list.append((edge[0], node_depth_list[-1][1]+1))
            forest.append(edge)

    # Then, expand the forest keeping minimal depth.
    while len(node_depth_list) != 0:
        node_depth_list = sorted(node_depth_list, key=lambda x: x[1])
        node_depth = node_depth_list.pop(0)
        for neighbour in reverse_adjacency_list[node_depth[0]]:
            if neighbour in visited:
                continue
            visited.add(neighbour)
            if node_depth[1] == max_depth:
                node_depth_list.append((neighbour, 0))
            else:
                node_depth_list.append((neighbour, node_depth[1]+1))
                forest.append((neighbour, node_depth[0]))
    
    return sorted(forest, key=lambda x: x[0])
