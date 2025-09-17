import cirq
import numpy as np
from typing import List, Dict, Union
from abc import ABC
from dataclasses import dataclass

from .simulator import *


class CirqSimulator(Simulator):
    def __init__(self):
        super(CirqSimulator, self).__init__()

