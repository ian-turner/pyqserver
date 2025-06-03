import numpy as np
from typing import Union
from abc import ABC, abstractmethod
from typing import List


class SimOp(ABC):
    """
    Simulator operation class
    """
    @classmethod
    def __repr__(cls):
        return '%s' % cls.__name__


class UnitaryOp(SimOp):
    """
    Unitary operation on a quantum state in simulator
    """
    def __init__(self, unitary: np.ndarray[np.complex64], register: int, controls: List[int]):
        self.unitary = unitary
        self.register = register
        self.controls = controls


class QInit(SimOp):
    """Initializes a qubit in a register"""
    def __init__(self, register: int, bvalue: int = 0):
        self.register = register
        self.bvalue = bvalue


class BInit(SimOp):
    """Initializes a bit in a register"""
    def __init__(self, register: int, bvalue: int = 0):
        self.register = register
        self.bvalue = bvalue


class NInit(SimOp):
    """Initializes a qubit from a bit"""
    def __init__(self, register: int):
        self.register = register


class Measure(SimOp):
    """Measure a qubit register"""
    def __init__(self, register: int):
        self.register = register


class Discard(SimOp):
    """Discard a bit or measure and discard a qubit"""
    def __init__(self, register: int):
        self.register = register


class Read(SimOp):
    """
    Send the value of bit register or measure
    and send value of quantum register
    """
    def __init__(self, register: int):
        self.register = register


class Simulator:
    def __init__(self):
        pass

    def reset(self):
        pass

    def execute(self, op: SimOp) -> Union[int, None]:
        print(op)