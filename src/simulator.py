import cirq
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
    def __init__(self, verbose: bool = False, lazy: bool = False):
        self.verbose = verbose
        self._initialize()

    def _initialize(self):
        self.context: Dict[Register, RegType] = dict()
        self.qubits: Dict[Register, Qubit] = dict()
        self.states: Dict[Qubit] = dict()
        self.bits: Dict[Register, Bit] = dict()
        
    def reset(self):
        self._initialize()

    def dump(self) -> str:
        pass

    def fresh(self) -> int:
        pass

    def new_qubit(self, reg: int, bvalue: bool = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register exists: %d' % reg)

        # allocating new qubit
        q = Qubit(reg)
        self.context[reg] = RegType.QUBIT
        self.qubits[reg] = q

        # TODO: setting binary value

    def new_bit(self, reg: int, bvalue: bool = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register exists: %d' % reg)
        
        # allocating new bit
        self.context[reg] = RegType.BIT
        self.bits[reg] = bvalue

    def measure(self, reg: int):
        pass

    def read(self, reg: int) -> int:
        if self.context[reg] == RegType.QUBIT:
            self.measure(reg)
        return self.bits[reg]