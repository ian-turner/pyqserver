from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
import numpy as np
from qiskit import QuantumCircuit, qasm3
from qiskit_aer import AerSimulator
from qiskit.quantum_info.states.statevector import Statevector

from .simulator import *


# defining some helper types
Qubit = int
Bit = bool
Register = int


@dataclass
class QubitRegister:
    qubit: int

    def __repr__(self) -> str:
        return 'QubitRegister(qubit=%s)' % self.qubit


@dataclass
class BitRegister:
    bit: Bit


class QiskitSimulator(Simulator):
    def __init__(self):
        self.reset()
        self._sim = AerSimulator()

    def _check_qubit_reg_exists(self, reg: Register):
        if reg not in self.context:
            raise UsageError('Register %d does not exist' % reg)
        
        if not isinstance(self.context[reg], QubitRegister):
            raise UsageError('Register %d must be of type Qubit' % reg)

    def _check_bit_reg_exists(self, reg: Register):
        if reg not in self.context:
            raise UsageError('Register %d does not exist' % reg)
        
        if not isinstance(self.context[reg], BitRegister):
            raise UsageError('Register %d must be of type Bit' % reg)

    def reset(self):
        """ Initialize simulator with an empty typing context
        and an empty quantum state """
        # creating empty typing context
        self.num_qubits = 0
        self.context: Dict[Register, Union[QubitRegister, BitRegister]] = dict()

        self.state = None

    def dump(self) -> str:
        """ Dump the entire simulator state to the console """
        context = ''
        for key in self.context:
            val = self.context[key]
            context += '\n%d: %s' % (key, val)

        if self.state == None:
            return context
        else:
            return context + '\nStatevector: ' + str(self.state.data) + '\n\n'

    def fresh(self) -> Register:
        """ Finds the first unused register """
        i = 0
        while True:
            if i not in self.context:
                break
            i += 1
        return i
    
    def new_qubit(self, reg: Register, bvalue: Bit = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)
        
        self.num_qubits += 1
        if self.state == None:
            # if state is none, just create the state vector manually
            if bvalue:
                self.state = Statevector([0, 1])
            else:
                self.state = Statevector([1, 0])
        else:
            qc = QuantumCircuit(self.num_qubits)
            qc.initialize(self.state, list(range(self.num_qubits-1)))
            if bvalue:
                qc.x(self.num_qubits-1)
            qc.save_statevector()
            self.state = self._sim.run(qc,shots=1).result().get_statevector()
        
        self.context[reg] = QubitRegister(self.num_qubits-1)