# Standard Library Imports
from __future__ import annotations
from typing import List

# Local Imports - panco libraries
from ecowcdb.panco.descriptor.curves import TokenBucket, RateLatency



class Server:
    """
    The Server class encodes the description of a server, characterized by:

        - a (minimal) service curve :math:`\\beta(t) = \\max_i(R_i(t-T_i)_+)`
        - a greedy shaping curve :math:`\\gamma(t) = \min_i (\\sigma_i + \\rho_i t)`

    :param service_curve: the service curve, given by a maximum of the rate-latency functions :math:`\\beta`.
    :type service_curve: List[RateLatency]
    :param max_service_curve: the maximum curve, given by a minimum of the token-bucket functions :math:`\\gamma`
    :type max_service_curve: List[TokenBucket]


    >>> Server([RateLatency(10, 1), RateLatency(20, 2)], [TokenBucket(5, 20), TokenBucket(0, 30)])
    <Server: β(t) = max [10(t - 1)_+, 20(t - 2)_+]
             \u03C3(t) = min [5 + 20t, 0 + 30t]>
    <BLANKLINE>
    """
    def __init__(self, service_curve: List[RateLatency], max_service_curve: List[TokenBucket]):
        self.service_curve = service_curve
        self.max_service_curve = max_service_curve

    def __str__(self) -> str:
        return "β(t) = max %s\n         \u03C3(t) = min %s" % (self.service_curve, self.max_service_curve)

    def __repr__(self) -> str:
        return "<Server: %s>\n" % self.__str__()

    def __eq__(self, other: Server):
        return self.max_service_curve == other.max_service_curve and self.service_curve == other.service_curve
