import cirq
from qsimcirq import QSimSimulator
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from qbraid.transpiler import transpile

from .simulator import *


class CirqSimulator(Simulator):
    def __init__(self):
        super(CirqSimulator, self).__init__()

    def dump(self):
        pass

    def _execute_qasm(self, qasm_str: str):
        qc = transpile(qasm_str, 'cirq')

        # state initialization...

        # running simulation
#        sim = cirq.Simulator()
        sim = QSimSimulator()
        result = sim.simulate(qc)

        # getting bit outputs
        bit_results = {}
        for key in result.measurements:
            idx = int(key.split('_')[1])
            bit_results[idx] = result.measurements[key].item()

        self.bit_register = {}
        for x in self.bit_map:
            self.bit_register[x] = bit_results[self.bit_map[x]]

        # saving statevector...

        # shifting qubit map down...
