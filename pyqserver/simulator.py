from abc import ABC, abstractmethod
from typing import Type
from dataclasses import dataclass, is_dataclass
from enum import Enum

from .parser import *


class UsageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Result(ABC):
    def __init_subclass__(cls: Type, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_dataclass(cls):
            dataclass(cls)

class Reply(Result):
    """Send reply string to user"""
    message: str

class Info(Result):
    """Send message string to user (meant for debugging)"""
    content: str

class OK(Result):
    """The instruction has executed properly"""

class Terminate(Result):
    """Shut down the simulator and close the connection"""

class Null(Result):
    """Nothing happened"""


class Simulator(ABC):
    def __init__(self):
        self.reset()

    @abstractmethod
    def dump(self):
        pass

    @abstractmethod
    def _execute_qasm(self):
        pass

    def reset(self):
        self.qubit_map = {}
        self.bit_map = {}
        self.queue = []
        self.num_prev_qubits = 0
        self.num_prev_bits = 0
        self.bit_register = {}

    def _command_to_qasm_gate(self, command: Command) -> str:
        match command:
            case Q():
                idx = self.free_qubits.pop()
                self.qubit_map[command.reg] = idx
                gate_str = 'reset qs[%d];' % idx
                if command.bvalue:
                    gate_str += '\nx qs[%d];' % idx
                return gate_str
            case M():
                bit_idx = self.free_bits.pop()
                qubit_idx = self.qubit_map[command.reg]
                self.bit_map[command.reg] = bit_idx
                del self.qubit_map[command.reg]
                self.free_qubits.append(qubit_idx)
                return 'bs[%d] = measure qs[%d];' % (bit_idx, qubit_idx)
            case X():
                idx = self.qubit_map[command.reg]
                return 'x qs[%d];' % idx
            case Y():
                idx = self.qubit_map[command.reg]
                return 'y qs[%d];' % idx
            case Z():
                idx = self.qubit_map[command.reg]
                return 'z qs[%d];' % idx
            case H():
                idx = self.qubit_map[command.reg]
                return 'h qs[%d];' % idx
            case S():
                idx = self.qubit_map[command.reg]
                return 's qs[%d];' % idx
            case SInv():
                idx = self.qubit_map[command.reg]
                return 'sdg qs[%d];' % idx
            case T():
                idx = self.qubit_map[command.reg]
                return 't qs[%d];' % idx
            case TInv():
                idx = self.qubit_map[command.reg]
                return 'tdg qs[%d];' % idx
            case Rot():
                idx = self.qubit_map[command.reg]
                return 'rz(%f) qs[%d];' % (command.r, idx)
            case CRot():
                x = self.qubit_map[command.x]
                y = self.qubit_map[command.y]
                return 'ctrl @ rz(%f) qs[%d], qs[%d];' % (command.r, x, y)
            case CNOT():
                x = self.qubit_map[command.x]
                y = self.qubit_map[command.y]
                return 'cx qs[%d], qs[%d];' % (x, y)
            case _:
                return ''

    def _commands_to_qasm(self, commands: List[Command]) -> str:
        header = 'OPENQASM 3.0;\ninclude "stdgates.inc";\n'

        num_prev_qubits = self.num_prev_qubits
        num_prev_bits = self.num_prev_bits
        max_qubits = 0
        bits = 0
        current_qubits = 0
       
        for command in commands:
            match command:
                case Q():
                    current_qubits += 1
                    if current_qubits > max_qubits:
                        max_qubits += 1
                case M():
                    current_qubits -= 1
                    bits += 1
                case D():
                    current_qubits -= 1
                case B():
                    bits += 1
        
        init_decls = 'qubit[%d] qs;\n' % (max_qubits + num_prev_qubits)
        if bits > 0:
            init_decls += 'bit[%d] bs;\n' % (bits + num_prev_bits)

        gate_strs = []
        self.free_qubits = list(range(num_prev_qubits, max_qubits + num_prev_qubits))
        self.free_bits = list(range(num_prev_bits, num_prev_bits + bits))
        for command in commands:
            gate_str = self._command_to_qasm_gate(command)
            gate_strs.append(gate_str)

        gate_strs_comb = '\n'.join(gate_strs)

        full_qasm = header + init_decls + gate_strs_comb
        return full_qasm

    def _execute_queue(self):
        if len(self.queue) == 0:
            return

        qasm_str = self._commands_to_qasm(self.queue)
        self._execute_qasm(qasm_str)
        self.queue = []

    def execute(self, command: Command):
        match command:
            case R():
                self._execute_queue()
                rval = self.bit_register[command.reg]
                del self.bit_register[command.reg]
                del self.bit_map[command.reg]
                self.num_prev_bits -= 1
                return Reply(str(rval))
            case Quit():
                return Terminate()
            case Reset():
                self.reset()
            case _:
                self.queue.append(command)

        return OK()
