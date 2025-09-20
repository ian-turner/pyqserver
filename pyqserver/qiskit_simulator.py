import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from qiskit import qasm3
from qiskit_aer import AerSimulator

from .simulator import *


class QiskitSimulator(Simulator):
    def __init__(self):
        super(QiskitSimulator, self).__init__()

    def dump(self):
        pass

    def _execute_qasm(self, qasm_str: str):
        sim = AerSimulator()
        qc = qasm3.loads(qasm_str)
        result = sim.run(qc, shots=1, memory=True).result()
        bit_result = [int(x) for x in result.get_memory()[0][::-1]]
        self.bit_register = {}
        for x in self.bit_map:
            self.bit_register[x] = bit_result[self.bit_map[x]]
