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


class Simulator:
    def __init__(self):
        pass

    def reset(self):
        pass

    def execute(self, op: SimOp) -> Union[int, None]:
        pass