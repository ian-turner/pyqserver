import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from qiskit import QuantumCircuit, qasm3, qpy
from qiskit_aer import AerSimulator
from qiskit.quantum_info import partial_trace

from .simulator import *


class QiskitSimulator(Simulator):
    def __init__(self):
        super(QiskitSimulator, self).__init__()

    def reset(self):
        super().reset()
        self.state = None

    def dump(self):
        pass

    def _execute_qasm(self, qasm_str: str):
        # loading qasm as a circuit
        qc = qasm3.loads(qasm_str)
        qc.save_statevector()
        if self.state and self.num_prev_qubits > 0:
            # prepending state initialization
            _qc = QuantumCircuit(self.num_prev_qubits)
            _qc.initialize(self.state, list(range(self.num_prev_qubits)))
            qc = _qc.compose(qc)

        with open('circ.qpy', 'wb') as file:
            qpy.dump(qc, file)

        # running simulation
        sim = AerSimulator()
        result = sim.run(qc, shots=1, memory=True).result()

        # getting bit outputs
        bit_result = [int(x) for x in result.get_memory()[0][::-1]]
        for x in self.bit_map:
            self.bit_register[x] = bit_result[self.bit_map[x]]

        # saving statevector for future computation
        sv = result.get_statevector()
        qubits_to_remove = list(range(qc.num_qubits))
        for x in self.qubit_map:
            qubits_to_remove.remove(self.qubit_map[x])

        sv_pruned = partial_trace(sv, qubits_to_remove).to_statevector()
        self.state = sv_pruned

        # shifting entire qubit map down
        qubit_map_list = [(x, self.qubit_map[x]) for x in self.qubit_map]
        qubit_map_list = sorted(qubit_map_list, key=lambda x: x[1])
        for i, x in enumerate(qubit_map_list):
            self.qubit_map[x[0]] = i

        self.num_prev_qubits = len(list(self.qubit_map))
        self.num_prev_bits = len(list(self.bit_map))
