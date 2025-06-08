import cirq
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass


# defining some helper types
Qubit = cirq.NamedQubit
Bit = bool
Register = int


@dataclass
class QubitRegister:
    qubit: cirq.NamedQubit

    def __repr__(self) -> str:
        return 'QubitRegister(qubit=%s)' % self.qubit.name


@dataclass
class BitRegister:
    bit: Bit


class UsageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Simulator:
    def __init__(self, verbose: bool = False):
        self.verbose = verbose
        self.reset()

    def reset(self):
        """ Initialize simulator with an empty typing context
        and an empty quantum state """
        # creating empty typing context
        self.context: Dict[Register, Union[QubitRegister, BitRegister]] = dict()

        # creating empty cirq simulator state
        self.state = cirq.StateVectorSimulationState(qubits=())

    def dump(self) -> str:
        """ Dump the entire simulator state to the console """
        state_vector = self.state._state._state_vector.flatten()
        context = ''
        for key in self.context:
            val = self.context[key]
            context += '\n\t\t%d: %s' % (key, val)
        return 'Simulator state:\n\tContext: %s\n\tState vector: %s\n' \
            % (context, str(state_vector))

    def fresh(self) -> Register:
        pass

    def new_qubit(self, reg: Register, bvalue: Bit = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)
        
        # creating a new qubit
        q = Qubit(str(reg))
        self.context[reg] = QubitRegister(q)

        # adding to current state
        self.state.add_qubits([q])

        # adding X gate if we want to initialize to 1
        if bvalue:
            self.state.apply_operation(cirq.X(q))

    def new_bit(self, reg: Register, bvalue: Bit = False):
        # making sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)
        
        # creating a new bit
        self.context[reg] = BitRegister(bvalue)

    def new_qubit_from_bit(self, reg: Register):
        # making sure register exists and is bit type
        if reg not in self.context:
            raise UsageError('Register %d does not exist' % reg)
        
        b_reg = self.context[reg]
        if not isinstance(b_reg, BitRegister):
            raise UsageError('Register %d is not type Bit' % reg)

        # removing bit register from context
        del self.context[reg]
        
        # creating new qubit register
        self.new_qubit(reg, b_reg.bit)

    def measure(self, reg: Register):
        # making sure register exists and is type qubit
        if reg not in self.context:
            raise UsageError('Register %d does not exist' % reg)
        
        q_reg = self.context[reg]
        if not isinstance(q_reg, QubitRegister):
            raise UsageError('Register %d must have type Qubit' % reg)
        
        # applying measurement operation
        q = q_reg.qubit
        self.state.apply_operation(cirq.measure(q, key='m'))
        meas_result: Bit = Bit(self.state.log_of_measurement_results['m'][0])

        # applying X gate if measure result is 1
        # (qubits must be |0> to be removed from state vector)
        if meas_result:
            self.state.apply_operation(cirq.X(q))

        # removing qubit from state vector
        self.state.remove_qubits([q])

        # converting type of register to bit
        self.context[reg] = BitRegister(meas_result)

    def read(self, reg: Register) -> int:
        # making sure register exists
        if reg not in self.context:
            raise UsageError('Register %d does not exist' % reg)
        
        # if the register is qubit, measure it first
        _reg = self.context[reg]
        if isinstance(_reg, QubitRegister):
            self.measure(reg)
        
        # then return the bit value of the register
        return int(self.context[reg].bit)