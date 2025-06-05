from typing import List
from dataclasses import dataclass

from parser import *


@dataclass
class Result:
    data: Union[int, None] = None


class Simulator:
    def __init__(self):
        pass

    def execute(self, commands: List[Command]) -> Result:
        pass