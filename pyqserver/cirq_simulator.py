import cirq
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass
from cirq.contrib.qasm_import import circuit_from_qasm

from .simulator import *


class CirqSimulator(Simulator):
    def __init__(self):
        super(CirqSimulator, self).__init__()

    def dump(self):
        pass

    def _execute_qasm(self, qasm_str: str):
        pass
