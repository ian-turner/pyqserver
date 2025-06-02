from typing import Union
from abc import ABC, abstractmethod


class SimOp(ABC):
    """
    Simulator operation class
    """


class BitOp(SimOp, ABC):
    """
    Operation on bit register in simulator
    """


class UnitaryOp(SimOp, ABC):
    """
    Unitary operation on a quantum state in simulator
    """


class MeasureOp(SimOp, ABC):
    """
    Operation involving measurement on a quantum state
    """


class QInit(SimOp):
    """Initializes a qubit in a register"""


class BInit(SimOp):
    """Initializes a bit in a register"""


class NInit(SimOp):
    """Initializes a qubit from a bit"""


class Measure(MeasureOp):
    """Measure a qubit register"""


class Discard(MeasureOp):
    """Discard a bit or measure and discard a qubit"""


class Read(MeasureOp):
    """
    Send the value of bit register or measure
    and send value of quantum register
    """


class Simulator:
    def __init__(self):
        pass

    def reset(self):
        pass

    def execute(self, op: SimOp) -> Union[int, None]:
        pass