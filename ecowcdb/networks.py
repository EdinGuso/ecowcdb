"""
 File containing Networks class which helps generate common network topologies. Esentially a wrapper around panco
 Network class.
"""

# Standard Library Imports
from itertools import product
from typing import List, Tuple

# Local Imports - ecowcdb libraries
from ecowcdb.options import NetworkType

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.curves import RateLatency, TokenBucket
from ecowcdb.panco.descriptor.flow import Flow
from ecowcdb.panco.descriptor.network import Network
from ecowcdb.panco.descriptor.server import Server

# Local Imports - utility libraries
from ecowcdb.util.validation import Validation



class Networks:
    """
     Base class for common network topologies. Can also be used for creating a custom network. The unit of latency is
     always assumed to be seconds. Rate and burst units are up to the user as long as `rate = burst / latency` is
     satisfied for the units. However, it is recommended to use kb/s for rate and kb for burst to ensure lp_solve
     has a higher chance of solving the generated lp files during the delay computations in Analysis.

     Methods:
         _generic (protected): Creates a generic network based on the provided parameters. Used by child classes.
         custom (public): Creates a custom network based on the provided parameters.
    """
    __validation: Validation.Networks

    def __init__(self) -> None:
        """
         Initialize the Validation.Networks object. This is the constructor for the class.
        """
        self.__validation = Validation.Networks()

    def _generic(self, R: float, L: float, S: float, N: int, load: float, max_flows: int, paths: List[List[int]],
                 network_type: NetworkType) -> Network:
        """
         Creates a generic network according to given parameters. This is the function that does the heavy lifting of the
         network creation.
        
         Args:
             R (float, required): Rate of the servers.
             L (float, required): Latency of the servers [seconds].
             S (float, required): Burst of the flows.
             N (int, required): Number of servers in the network.
             load (float, required): Maximum load allowed on a server.
             max_flows (int, required): Maximum number of flows crossing any server.
             paths (List[List[int]], required): List of paths to create flows for.
             network_type (NetworkType, required): Type of network to create.
        
         Returns: 
             Network: A generic network generated according to the input parameters.
        """
        ASYMMETRICITY_FACTOR = 0.8

        service_curve = RateLatency(R, L)
        shaper = TokenBucket(0, R)
        server = Server([service_curve], [shaper])
        servers = N * [server]

        arrival_curve = TokenBucket(S, load * R / max_flows)
        flows = [Flow([arrival_curve], p) for p in paths]

        match network_type:
            case NetworkType.Symmetric:
                pass
            case NetworkType.AsymmetricFlow:
                # Every flow has decreased rate except for first flow. First flow dominates.
                for i in range(1,len(flows)):
                    flows[i] = Flow([TokenBucket(flows[i].arrival_curve[0].sigma,
                                                 ASYMMETRICITY_FACTOR * flows[i].arrival_curve[0].rho)], flows[i].path)
            case NetworkType.AsymmetricServer:
                # Every server has increased rate except for first flow. First server is bottleneck.
                for i in range(1, len(servers)):
                    servers[i] = Server(
                            [RateLatency(servers[i].service_curve[0].rate/ASYMMETRICITY_FACTOR,
                                         servers[i].service_curve[0].latency)],
                            [TokenBucket(0, servers[i].max_service_curve[0].rho/ASYMMETRICITY_FACTOR)])
            case _:
                raise ValueError(f'Unhandled network type: {network_type}')
        return Network(servers, flows)
            
    def custom(self, servers_args: List[Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]],
               flows_args: List[Tuple[List[Tuple[float, float]], List[int]]]) -> Network:
        """
         Create a custom network. This is the function that does the heavy lifting of the network creation.
         
         Args:
         	 servers_args (List[Tuple[List[Tuple[float, float]], List[Tuple[float, float]]]], required): List of server
             args. Each element of the list is a tuple consisting of list of service curve args and list of shaper
             args. Service curve args are tuples of two non-negative ints. Shaper args are tuples of two non-negtive
             ints.
         	 flows_args (List[Tuple[List[Tuple[float, float]], List[int]]], required): List of flow args. Each element
             of the list is a tuple consisting of list of arrival curve args and a path. Arrival curve args are tuples
             of two non-negative integers. Path is a list of non-negative integerers upper bounded by number of
             servers.
         
         Returns: 
         	 Network: A custom network generated according to the input parameters.
        """
        self.__validation.custom_network_arguments(servers_args, flows_args)
        servers = []
        for server_args in servers_args:
            service_curves = []
            for service_curve_args in server_args[0]:
                service_curves.append(RateLatency(service_curve_args[0], service_curve_args[1]))
            shapers = []
            for shaper_args in server_args[1]:
                shapers.append(TokenBucket(shaper_args[0], shaper_args[1]))
            servers.append(Server(service_curves, shapers))

        flows = []
        for flow_args in flows_args:
            arrival_curves = []
            for arrival_curve_args in flow_args[0]:
                arrival_curves.append(TokenBucket(arrival_curve_args[0], arrival_curve_args[1]))
            path = flow_args[1]
            flows.append(Flow(arrival_curves, path))

        return(Network(servers, flows))


    class Tandem:
        """
         Class for creating tandem networks. Tandem networks are networks arranged on a straight line. After creating
         an object of the class, one can use that object to generate different types of tandem networks.

         Attributes:
             __validation (Validation, private): Validation object used to validate user inputs.

         Methods:
             sink_tree (public): Creates a sink-tree tandem network.
             interleaved (public): Creates an interleaved tandem network.
             source_sink (public): Creates a source-sink tandem network.
        """
        __validation = Validation.Networks
        # __networks = Networks

        def __init__(self) -> None:
            """
             Initialize the Validation.Networks and Networks objects. This is the constructor for the class.
            """
            self.__validation = Validation.Networks()
            self.__networks = Networks()

        def sink_tree(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a sink-tree tandem network. Sink-tree tandem networks have a flow starting at each server, all
             ending at the sink.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: A sink tree network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []
            for i in range(N):
                paths.append(list(range(i, N)))
            
            max_flows = N # 1,2,..,N
            
            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)

        def interleaved(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates am interleaved tandem network. Interleaved tandem networks have one long flow going through the
             entire network, and N-1 2-length flows between consecutive servers.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: An interleaved network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            paths = [list(range(N))]
            for i in range(N-1):
                paths.append([i, i+1])

            max_flows = 3 # 3...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)
        
        def source_sink(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a source-sink tandem network. Source-sink tandem networks have one long flow going through the
             entire network, and N-1 pairs of flows where first flow in each pair starts at the source, and second flow
             starts where the first one ended and ends at the sink.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: A source-sink network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            paths = [list(range(N))]
            for i in range(1,N):
                paths.append(list(range(0, i)))
                paths.append(list(range(i, N)))

            max_flows = N # N...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)


    class Mesh:
        """
         Class for creating mesh networks. Mesh networks have two rows of servers and a sink server. After creating an
         object of the class, one can use that object to generate different types of mesh networks.

         Attributes:
             __validation (Validation, private): Validation object used to validate user inputs.

         Methods:
             simple (public): Creates a simple mesh network.
        """
        __validation = Validation.Networks

        def __init__(self) -> None:
            """
             Initialize the Validation.Networks object. This is the constructor for the class.
            """
            self.__validation = Validation.Networks()

        def simple(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a simple mesh network. Simple mesh networks have flows starting at either row's source and at each
             step either continues along the row or switches to the other row, and ends at the sink server. Simple mesh
             networks have 2N+1 servers. Does not support asymmetric network types.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Length of the rows of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.

             Raises:
                 NotImplementedError: If network type is not Symmetric.
            
             Returns:
                 Network: A simple mesh network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            if network_type != NetworkType.Symmetric:
                raise NotImplementedError('Asymmetric mesh networks not supported yet')

            paths = [list(path) + [2*N] for path in list(product(*[(2*i,2*i+1) for i in range(N)]))]

            service_curve = RateLatency(R, L)
            shaper = TokenBucket(0, R)
            server = Server([service_curve], [shaper])

            sink_service_curve = RateLatency(2*R, L)
            sink_shaper = TokenBucket(0, 2*R)
            sink_server = Server([sink_service_curve], [sink_shaper])

            arrival_curve = TokenBucket(S, load * R / (2**(N-1)))
            flows = [Flow([arrival_curve], p) for p in paths]

            return Network(2 * N * [server] + [sink_server], flows)


    class Ring:
        """
         Class for creating ring networks. Ring networks are topologically a cycle and all the flows are in the same
         direction. After creating an object of the class, one can use that object to generate different types of ring
         networks.

         Attributes:
             __validation (Validation, private): Validation object used to validate user inputs.

         Methods:
             full (public): desc.
             semi (public): desc.
             complete_full (public): desc.
             complete_semi (public): desc.
        """
        __validation = Validation.Networks
        # __networks = Networks

        def __init__(self) -> None:
            """
             Initialize the Validation.Networks and Networks objects. This is the constructor for the class.
            """
            self.__validation = Validation.Networks()
            self.__networks = Networks()

        def full(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a full ring network. Full ring networks have N topologically symmetric, circular flows of length
             N-1.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: A full ring network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            paths = []
            for i in range(N):
                paths.append([p % N for p in list(range(i, i+N))])

            max_flows = N # N...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)
        
        def semi(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a semi ring network. Semi ring networks have N topologically symmetric, circular flows of length
             N//2.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: A semi ring network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []
            for i in range(N):
                paths.append([p % N for p in list(range(i, i+N//2+1))])

            max_flows = N//2 + 1 # N//2+1...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)

        def complete_full(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a complete full ring network. Complete full ring networks have N*N flows. There are N flows
             starting from each server, and lengths of these servers go from 0 to N-1. If you consider the same
             length flows, they are topologically symmetric, circular flows.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: A complete full ring network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []
            for i in range(N):
                for j in range(i + N, i, -1):
                    paths.append([p % N for p in list(range(i, j))])

            max_flows = N * (N + 1) // 2 # N*(N+1)//2...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)

        def complete_semi(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            """
             Creates a complete semi ring network. Complete semi ring networks have N*(N//2+1) flows. There are N//2+1
             flows starting from each server, and lengths of these servers go from 0 to N//2. If you consider the same
             length flows, they are topologically symmetric, circular flows.
             
             Args:
                 R (float, required): Rate of the servers.
                 L (float, required): Latency of the servers [seconds].
                 S (float, required): Burst of the flows.
                 N (int, required): Number of servers in the network.
                 load (float, required): Maximum load allowed on a server.
                 network_type (NetworkType, required): Type of network to create.
            
             Returns:
                 Network: A complete semi ring network.
            """
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []
            for i in range(N):
                for j in range(i + N//2 + 1, i, -1):
                    paths.append([p % N for p in list(range(i, j))])

            max_flows = ((N//2 + 1) * (N//2 + 2)) // 2 # ((N//2+1)*(N//2+2))//2...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)
        