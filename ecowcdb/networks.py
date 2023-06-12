# Standard Library Imports
from itertools import product
from typing import List

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

    def custom(self, servers: List[Server], flows: List[Flow]):
        return(Network(servers, flows))

    def _generic(self, R: float, L: float, S: float, N: int, load: float, max_flows: int, paths: List[List[int]], network_type: NetworkType) -> Network:

        ASYMMETRICITY_FACTOR = 0.8

        service_curve = RateLatency(R, L)
        shaper = TokenBucket(0, R)
        server = Server([service_curve], [shaper])
        servers = N * [server]

        arrival_curve = TokenBucket(S, load * R / max_flows)
        flows = [Flow([arrival_curve], p) for p in paths]

        match network_type:
            case NetworkType.Symmetric:
                return Network(servers, flows)
            case NetworkType.AsymmetricFlow:
                # Every flow has decreased rate except for first flow. First flow dominates
                for i in range(1,len(flows)):
                    flows[i] = Flow([TokenBucket(flows[i].arrival_curve[0].sigma, ASYMMETRICITY_FACTOR * flows[i].arrival_curve[0].rho)], flows[i].path)
                return Network(servers, flows)
            case NetworkType.AsymmetricServer:
                # Every server has increased rate except for first flow. First server is bottleneck
                for i in range(1, len(servers)):
                    servers[i] = Server([RateLatency(servers[i].service_curve[0].rate/ASYMMETRICITY_FACTOR, servers[i].service_curve[0].latency)], [TokenBucket(0, servers[i].max_service_curve[0].rho/ASYMMETRICITY_FACTOR)])
                return Network(servers, flows)
            case _:
                raise ValueError(f'Unhandled network type: {network_type}')

    def empty(self) -> Network:
        return Network([], [])


    class Tandem:
        def __init__(self) -> None:
            self.__validation = Validation.Networks()
            self.__networks = Networks()

        def sink_tree(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []

            for i in range(N):
                paths.append(list(range(i, N)))

            max_flows = N # 1,2,..,N

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)

        def interleaved(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            paths = [list(range(N))]

            for i in range(N-1):
                paths.append([i, i+1])

            max_flows = 3 # 3...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)
        
        def source_sink(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            paths = [list(range(N))]

            for i in range(1,N):
                paths.append(list(range(0, i)))
                paths.append(list(range(i, N)))

            max_flows = N # N...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)



    class Mesh:
        def __init__(self) -> None:
            self.__validation = Validation.Networks()
            self.__networks = Networks()

        def simple(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            if network_type != NetworkType.Symmetric:
                raise NotImplementedError('Asymmetric mesh networks not supported yet')

            paths = [list(path) + [2*N] for path in list(product(*[(2*i,2*i+1) for i in range(N)]))]

            service_curve = RateLatency(R, L)
            shaper = TokenBucket(0, R)
            server = Server([service_curve], [shaper])

            sink_service_curve = RateLatency(2*R, L)
            sink_server = Server([sink_service_curve], [shaper])

            arrival_curve = TokenBucket(S, load * R / (2**(N-1)))
            flows = [Flow([arrival_curve], p) for p in paths]

            return Network(2 * N * [server] + [sink_server], flows)



    class Ring:
        def __init__(self) -> None:
            self.__validation = Validation.Networks()
            self.__networks = Networks()

        def full(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)

            paths = []

            for i in range(N):
                paths.append([p % N for p in list(range(i, i+N))])

            max_flows = N # N...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)
        
        def semi(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []

            for i in range(N):
                paths.append([p % N for p in list(range(i, i+N//2+1))])

            max_flows = N//2 + 1 # N//2+1...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)

        def complete_full(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []

            for i in range(N):
                for j in range(i + N, i, -1):
                    paths.append([p % N for p in list(range(i, j))])

            max_flows = N * (N + 1) // 2 # N*(N+1)//2...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)

        def complete_semi(self, R: float, L: float, S: float, N: int, load: float, network_type: NetworkType) -> Network:
            self.__validation.generic_arguments(R, L, S, N, load, network_type)
            
            paths = []

            for i in range(N):
                for j in range(i + N//2 + 1, i, -1):
                    paths.append([p % N for p in list(range(i, j))])

            max_flows = ((N//2 + 1) * (N//2 + 2)) // 2 # ((N//2+1)*(N//2+2))//2...

            return self.__networks._generic(R, L, S, N, load, max_flows, paths, network_type)
        