from abc import ABC


class UsageError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


class Simulator(ABC):
    pass