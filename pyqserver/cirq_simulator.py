import cirq
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from cirq.contrib.qasm_import import circuit_from_qasm

from .simulator import *


class CirqSimulator(Simulator):
    def __init__(self, queueing=False):
        super(CirqSimulator, self).__init__(queueing=queueing)

    def reset(self):
        super().reset()
        self.state = np.array([1], dtype=np.complex64)

    def dump(self):
        pass

    def _measure(self, reg: int):
        # measuring the state and collapsing the state vector
        result, sv = cirq.measure_state_vector(self.state, [self.qubit_map[reg]])
        bit_result = result[0]
        self.bit_register[reg] = bit_result

        # removing qubit from state vector
        if self.num_qubits > 1:
            prune_idxs = [np.s_[:]] * self.num_qubits
            prune_idxs[self.qubit_map[reg]] = bit_result
            prune_idxs
            dims = [2] * self.num_qubits
            sv_reshaped = sv.reshape(dims)
            new_sv = sv_reshaped[*prune_idxs].flatten()
            self.state = new_sv

            # shifting qubit map down to fill space of removed qubit
            for x in self.qubit_map:
                if self.qubit_map[x] > self.qubit_map[reg]:
                    self.qubit_map[x] -= 1
        
        else:
            self.state = np.array([1], dtype=np.complex64)

        self.num_qubits -= 1
        del self.qubit_map[reg]

    def _execute_qasm(self, qasm_str: str):
        # loading OpenQASM circuit
        qc = circuit_from_qasm(qasm_str)

        # loading previous statevector
        sv = None
        if len(self.state) > 1:
            num_prev_qubits = int(np.log2(self.state.shape[0]))
            new_sv = np.zeros(2**(self.num_qubits-num_prev_qubits), dtype=np.complex64)
            new_sv[0] = 1
            sv = np.kron(self.state, new_sv)

        # running simulation and saving statevector for future computation
        sim = cirq.Simulator()
        result = sim.simulate(qc, initial_state=sv)
        self.state = result.final_state_vector
