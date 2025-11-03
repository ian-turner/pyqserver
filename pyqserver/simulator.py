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
    def __init__(self, queueing=False):
        self.reset()
        self.queueing = queueing

    @abstractmethod
    def dump(self):
        pass

    @abstractmethod
    def _execute_qasm(self):
        pass

    @abstractmethod
    def _measure(self, reg: int):
        pass

    def reset(self):
        self.num_qubits = 0
        self.qubit_map = {}
        self.bit_register = {}
        self.queue = []

    def _command_to_qasm_gate(self, command: Command) -> str:
        match command:
            case Q():
                if command.bvalue:
                    return 'x qs[%d];' % self.qubit_map[command.reg]
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
                return 'cp(%f) qs[%d], qs[%d];' % (command.r, x, y)
            case CNOT():
                x = self.qubit_map[command.x]
                y = self.qubit_map[command.y]
                return 'cx qs[%d], qs[%d];' % (x, y)
            case Toffoli():
                x = self.qubit_map[command.x]
                y = self.qubit_map[command.y]
                z = self.qubit_map[command.z]
                return 'ccx qs[%d], qs[%d], qs[%d];' % (x, y, z)
            case _:
                return ''

    def _commands_to_qasm(self, commands: List[Command]) -> str:
        # calculating how many qubits to allocate for simulation
        for command in commands:
            match command:
                case Q():
                    self.qubit_map[command.reg] = self.num_qubits
                    self.num_qubits += 1

        # constrution OpenQASM circuit
        qasm_stmts = ['OPENQASM 3.0;', 'include "stdgates.inc";']
        qasm_stmts.append('qubit[%d] qs;' % self.num_qubits)
        qasm_stmts.append('id qs;') # temporary fix for cirq issue where qubits don't show up unless gates act on them
        for command in commands:
            stmt = self._command_to_qasm_gate(command)
            if stmt:
                qasm_stmts.append(stmt)

        qasm_str = '\n'.join(qasm_stmts)
        return qasm_str

    def _execute_queue(self):
        # do nothing if there are no commands in the queue
        if len(self.queue) > 0:
            qasm_str = self._commands_to_qasm(self.queue)
            self._execute_qasm(qasm_str)
            self.queue = []

    def execute(self, command: Command):
        match command:
            case M():
                self._execute_queue()
                self._measure(command.reg)
                return OK()
            case R():
                rval = self.bit_register[command.reg]
                del self.bit_register[command.reg]
                return Reply(str(rval))
            case Quit():
                return Terminate()
            case Reset():
                self.reset()
                return OK()
            case _:
                self.queue.append(command)
                if not self.queueing:
                    self._execute_queue()
                return OK()
