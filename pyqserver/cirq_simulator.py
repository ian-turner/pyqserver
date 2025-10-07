import cirq
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass

from .simulator import *


# defining some helper types
Qubit = cirq.NamedQubit
Bit = bool
Register = int


@dataclass
class QubitRegister:
    qubit: Qubit

    def __repr__(self) -> str:
        return 'QubitRegister(qubit=%s)' % self.qubit.name


@dataclass
class BitRegister:
    bit: Bit


class CirqSimulator(Simulator):
    def __init__(self):
        super(CirqSimulator, self).__init__()
        self.reset()

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
        
    def _gate_operation(self, gate, regs: List[Register], controls: List[Register]):
#        for x in regs:
#            self._check_qubit_reg_exists(x)
#        for c in controls:
#            self._check_bit_reg_exists(c)
#            c_reg = self.context[c]
#            if not c_reg.bit:
#                return
        qubits = [self.context[x].qubit for x in regs]
        self.state.apply_operation(gate(*qubits))

    def reset(self):
        """ Initialize simulator with an empty typing context
        and an empty quantum state """
        # creating empty typing context
        self.context: Dict[Register, Union[QubitRegister, BitRegister]] = dict()

        # creating empty cirq simulator state
        self.state = cirq.StateVectorSimulationState(qubits=())

    def dump(self) -> str:
        """ Dump the entire simulator state to the console """
        state_vector = self.state._state._state_vector.reshape(-1,1)
        context = ''
        for key in self.context:
            val = self.context[key]
            context += '\n%d: %s' % (key, val)
        # making sure to only print 100 lines of numpy vector
        with np.printoptions(threshold=100):
            return 'Simulator state:\nContext: %s\nState vector:\n%s\n' \
                % (context, str(state_vector))

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
#        if reg in self.context:
#            raise UsageError('Register %d already exists' % reg)
        
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
#        if reg in self.context:
#            raise UsageError('Register %d already exists' % reg)
        
        # creating a new bit
        self.context[reg] = BitRegister(bvalue)

    def new_qubit_from_bit(self, reg: Register):
        # making sure register exists and is bit type
#        self._check_bit_reg_exists(reg)

        # removing bit register from context
        del self.context[reg]
        
        # creating new qubit register
        self.new_qubit(reg, b_reg.bit)

    def measure(self, reg: Register):
        # making sure register exists and is type qubit
#        self._check_qubit_reg_exists(reg)
        q_reg = self.context[reg]
        
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
#        if reg not in self.context:
#            raise UsageError('Register %d does not exist' % reg)
        
        # if the register is qubit, measure it first
        _reg = self.context[reg]
        if isinstance(_reg, QubitRegister):
            self.measure(reg)
        
        # then return the bit value of the register
        return int(self.context[reg].bit)
    
    def discard(self, reg: Register):
        # making sure register exists
#        if reg not in self.context:
#            raise UsageError('Register %d does not exist' % reg)
        
        # if reg is qubit type, measure it first
        _reg = self.context[reg]
        if isinstance(_reg, QubitRegister):
            self.measure(reg)

        # removing bit register from context
        del self.context[reg]

    def gate_H(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.H, [reg], controls)

    def gate_X(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.X, [reg], controls)

    def gate_Y(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.Y, [reg], controls)

    def gate_Z(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.Z, [reg], controls)

    def gate_T(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.T, [reg], controls)

    def gate_TInv(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.inverse(cirq.T), [reg], controls)

    def gate_S(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.S, [reg], controls)

    def gate_SInv(self, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.inverse(cirq.S), [reg], controls)

    def gate_CNOT(self, x: Register, y: Register, controls: List[Register]):
        self._gate_operation(cirq.CNOT, [x, y], controls)

    def gate_Toffoli(self, x: Register, y: Register, z: Register, controls: List[Register]):
        self._gate_operation(cirq.TOFFOLI, [x, y, z], controls)
    
    def gate_Rz(self, r: float, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.Rz(rads=r), [reg], controls)

    def gate_Diag(self, a: float, b: float, reg: Register, controls: List[Register]):
        self._gate_operation(cirq.DiagonalGate(diag_angles_radians=[a, b]), [reg], controls)

    def gate_CZ(self, x: Register, y: Register, controls: List[Register]):
        self._gate_operation(cirq.CZ, [x, y], controls)
    
    def gate_CY(self, x: Register, y: Register, controls: List[Register]):
        self._gate_operation(cirq.Y.controlled(), [x, y], controls)
    
    def gate_CRz(self, r: float, x: Register, y: Register, controls: List[Register]):
        self._gate_operation(cirq.Rz(rads=r).controlled(num_controls=1), [x, y], controls)
