import cirq
import numpy as np
from typing import List, Dict
from enum import Enum


# definining bit and qubit types
Qubit = cirq.NamedQubit
Bit = bool
Register = int


class RegType(Enum):
    BIT = 0
    QUBIT = 1


class UsageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Simulator:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self._initialize()

    def _initialize(self):
        """ Initialize simulator with an empty typing context
        and an empty quantum state """
        # creating empty typing context
        self.context: Dict[Register, RegType] = dict()
        self.qubits: Dict[Register, Qubit] = dict()
        self.bits: Dict[Register, Bit] = dict()

        # creating empty cirq simulator state
        self.state = cirq.StateVectorSimulationState(qubits=())

    def reset(self):
        self._initialize()

    def dump(self) -> str:
        """ Dump the entire simulator state to the console """
        state_vector = self.state._state._state_vector.flatten()
        return 'Simulator state:\n\tContext: %s\n\tBits: %s\n\tState vector: %s\n' \
            % (str(self.context), str(self.bits), str(state_vector))

    def fresh(self) -> int:
        pass

    def new_qubit(self, reg: int, bvalue: bool = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)
        
        # creating a new qubit
        q = Qubit(str(reg))
        self.context[reg] = RegType.QUBIT
        self.qubits[reg] = q

        # adding to current state
        self.state.add_qubits([q])

        # adding X gate if we want to initialize to 1
        if bvalue:
            self.state.apply_operation(cirq.X(q))

    def new_bit(self, reg: int, bvalue: bool = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)
        
        # creating a new bit
        self.bits[reg] = bvalue

    def measure(self, reg: int):
        pass

    def read(self, reg: int) -> int:
        pass