import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from qiskit import QuantumCircuit, qasm3
from qiskit_aer import AerSimulator
from qiskit.quantum_info import Statevector

from .simulator import *


class QiskitSimulator(Simulator):
    def __init__(self, queueing=False):
        super(QiskitSimulator, self).__init__(queueing=queueing)

    def reset(self):
        super().reset()
        self.state = None

    def dump(self):
        pass

    def _measure(self, reg: int):
        # measuring the state and collapsing the state vector
        result, sv = self.state.measure([self.qubit_map[reg]])
        bit_result = int(result)
        self.bit_register[reg] = bit_result

        # removing qubit from state vector
        if self.num_qubits > 1:
            prune_idxs = [np.s_[:]] * self.num_qubits
            prune_idxs[self.qubit_map[reg]] = bit_result
            prune_idxs.reverse()
            sv_reshaped = sv.data.reshape(sv.dims())
            new_sv = sv_reshaped[*prune_idxs].flatten()
            self.state = Statevector(new_sv)

            # shifting qubit map down to fill space of removed qubit
            for x in self.qubit_map:
                if self.qubit_map[x] > self.qubit_map[reg]:
                    self.qubit_map[x] -= 1
        
        else:
            self.state = None

        self.num_qubits -= 1
        del self.qubit_map[reg]

    def _execute_qasm(self, qasm_str: str):
        # loading qasm as a circuit
        qc = qasm3.loads(qasm_str)
        qc.save_statevector()

        if self.state:
            qc_init = QuantumCircuit(self.num_qubits)
            num_prev_qubits = len(self.state.dims())
            qc_init.initialize(self.state, list(range(num_prev_qubits)))
            qc = qc_init.compose(qc)

        # running simulation
        sim = AerSimulator()
        result = sim.run(qc).result()

        # saving statevector for future computation
        self.state = result.get_statevector()
