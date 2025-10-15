import cirq
from qsimcirq import QSimSimulator
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from cirq.contrib.qasm_import import circuit_from_qasm

from .simulator import *


class CirqSimulator(Simulator):
    def __init__(self):
        super(CirqSimulator, self).__init__()

    def reset(self):
        super().reset()
        self.state = np.array([1], dtype=np.complex64)

    def dump(self):
        pass

    def _execute_qasm(self, n_qubits: int, qasm_str: str):
        qc = circuit_from_qasm(qasm_str)

        # state initialization...
        new_qubits = n_qubits - self.num_prev_qubits
        for _ in range(new_qubits):
            self.state = np.kron(self.state, np.array([1, 0], dtype=np.complex64))
        qs = list(qc.all_qubits())
        qc.insert(0, [cirq.StatePreparationChannel(self.state)(*qs)])

        # running simulation
#        sim = cirq.Simulator()
        sim = QSimSimulator()
        result = sim.run(qc)

        # getting bit outputs
        bit_results = {}
        for key in result.measurements:
            idx = int(key.split('_')[1])
            bit_results[idx] = result.measurements[key].item()

        self.bit_register = {}
        for x in self.bit_map:
            mapped_bit = self.bit_map[x]
            if mapped_bit in bit_results:
                self.bit_register[x] = bit_results[mapped_bit]
            else:
                self.bit_register[x] = 0

        # saving statevector...

        # shifting qubit map down
        qubit_map_list = [(x, self.qubit_map[x]) for x in self.qubit_map]
        qubit_map_list = sorted(qubit_map_list, key=lambda x: x[1])
        for i, x in enumerate(qubit_map_list):
            self.qubit_map[x[0]] = i

        self.num_prev_qubits = len(list(self.qubit_map))
        self.num_prev_bits = len(list(self.bit_map))
