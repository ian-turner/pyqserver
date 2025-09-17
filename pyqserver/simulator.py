from abc import ABC
from typing import Type
from dataclasses import dataclass, is_dataclass
from enum import Enum

from .parser import Command


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

class RegType(Enum):
    BIT = 1
    QUBIT = 2


class Simulator(ABC):
    def __init__(self):
        self.context = {}

    def _check_reg_exists(self, reg: int):
        if reg not in self.context:
            raise UsageError('Register %d does not exist' % reg)

    def _check_bit_exists(self, reg: int):
        self._check_reg_exists(reg)
        if self.context[reg] != RegType.BIT:
            raise UsageError('Register %d must be of type bit' % reg)

    def _check_qubit_exists(self, reg: int):
        self._check_reg_exists(reg)
        if self.context[reg] != RegType.QUBIT:
            raise UsageError('Register %d must be of type bit' % reg)

    def reset(self):
        self.context = {}

    def dump(self):
        pass

    def new_bit(self, reg: int, bvalue: bool = False):
        # make sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)

        # creating new bit in register
        self.context[reg] = RegType.BIT

        # creating new bit in simulator...

    def new_qubit(self, reg: int, bvalue: bool = False):
        # make sure register is empty
        if reg in self.context:
            raise UsageError('Register %d already exists' % reg)

        # creating new qubit in register
        self.context[reg] = RegType.QUBIT

        # creating new qubit in simulator...

    def execute(self, command: Command):
        return OK()
