from abc import ABC
from dataclasses import dataclass, is_dataclass

from parser import *
from simulator import *


class Response(ABC):
    def __init_subclass__(cls: Type, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_dataclass(cls):
            dataclass(cls)


class Reply(Response):
    data: int


class OK(Response):
    pass


class Terminate(Response):
    pass


class UsageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def interpret_command(command: Command, simulator: Simulator) -> Response:
    pass