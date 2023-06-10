#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# This file is part of the panco project.
# https://github.com/Huawei-Paris-Research-Center/Panco

from __future__ import annotations

__author__ = "Anne Bouillard"
__maintainer__ = "Anne Bouillard"
__email__ = "anne.bouillard@huawei.com"
__copyright__ = "Copyright (C) 2022, Huawei Technologies France"
__license__ = "BSD-3"

import subprocess as sp

from ecowcdb.panco.fifo.elpConstraints import ELPConstraints
from ecowcdb.panco.fifo.plpConstraints import PLPConstraints
from ecowcdb.panco.fifo.sfaLP import SfaLP
from ecowcdb.panco.fifo.tfaLP import TfaLP
from ecowcdb.panco.lpSolvePath import LPSOLVEPATH

from ecowcdb.util.errors import check_LP_error


class TreeLP:
    # Linear analysis for fifo tree networks
    def __init__(self, network, foi, polynomial=True, sfa=False, tfa=False, timeout=600, temp_folder="", filename="tree", verbose=False):
        self.network = network
        self.foi = foi
        # self.constraints = LPConstraints(network, foi)
        if sfa:
            delay_sfa = SfaLP(network, temp_folder=temp_folder, filename=filename+"_sfa", verbose=verbose).all_delays
        else:
            delay_sfa = None
        if tfa:
            delay_tfa = TfaLP(network, temp_folder=temp_folder, filename=filename+"_tfa", verbose=verbose).delay_servers
        else:
            delay_tfa = None
        if polynomial:
            self.constraints = PLPConstraints(network, foi, None, None, delay_sfa, delay_tfa)
        else:
            self.constraints = ELPConstraints(network, foi)
        self.timeout = timeout
        self.temp_folder = temp_folder
        self.filepath_delay = temp_folder + filename + "_delay.lp"
        self.filepath_backlog = temp_folder + filename + "_backlog.lp"
        self.verbose = verbose

    def burst_constraints(self, file):
        for i in range(self.network.num_flows):
            file.write('x{0} = {1};\n'.format(i, self.network.flows[i].arrival_curve[0].sigma))

    def delay_objective(self, file):
        if self.network.path[self.foi][-1] == self.network.num_servers - 1:
            file.write('max: t0e0 - t{}e0;\n'.format(self.constraints.t_min[self.network.path[self.foi][0]]))
        else:
            file.write('flow do not stop at last server\n')

    @property
    def delay(self):
        file = open(self.filepath_delay, 'w')
        self.delay_objective(file)
        self.constraints.time_constraints(file)
        self.constraints.arrival_constraints(file)
        self.constraints.fifo_constraints(file)
        self.constraints.service_constraints(file)
        self.constraints.monotony_constraints(file)
        self.constraints.shaping_constraints(file)
        self.constraints.arrival_shaping_constraints(file, True)
        self.constraints.sfa_delay_constraints(file)
        self.constraints.tfa_delay_constraints(file)
        self.burst_constraints(file)
        file.close()

        if self.verbose:
            print('Solving:', self.filepath_delay)

        s = sp.run(LPSOLVEPATH + ["-timeout", f"{self.timeout}", "-S1", self.filepath_delay], stdout=sp.PIPE, encoding='utf-8').stdout

        check_LP_error(s)

        return float(s.split()[-1])

    @property
    def backlog(self):
        file = open(self.filepath_backlog, 'w')
        self.constraints.backlog_objective(file)
        self.constraints.time_constraints(file)
        self.constraints.arrival_constraints(file)
        self.constraints.fifo_constraints(file)
        self.constraints.service_constraints(file)
        self.constraints.monotony_constraints(file)
        self.constraints.shaping_constraints(file)
        self.constraints.arrival_shaping_constraints(file, True)
        self.constraints.sfa_delay_constraints(file)
        self.constraints.tfa_delay_constraints(file)
        self.burst_constraints(file)
        file.close()

        if self.verbose:
            print('Solving:', self.filepath_backlog)

        s = sp.run(LPSOLVEPATH + ["-timeout", f"{self.timeout}", "-S1", self.filepath_backlog], stdout=sp.PIPE, encoding='utf-8').stdout
        
        check_LP_error(s)

        return float(s.split()[-1])
