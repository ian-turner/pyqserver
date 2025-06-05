from abc import ABC
from typing import List, Union
from dataclasses import dataclass


@dataclass
class Command(ABC):
    pass


@dataclass
class Help(Command):
    pass


@dataclass
class Empty(Command):
    pass


@dataclass
class Reset(Command):
    pass


@dataclass
class Fresh(Command):
    pass


@dataclass
class Protocol(Command):
    protocol: int


@dataclass
class Quit(Command):
    pass


@dataclass
class Dump(Command):
    pass


@dataclass
class Q(Command):
    reg: int
    bvalue: bool = False


@dataclass
class B(Command):
    reg: int
    bvalue: bool = False


@dataclass
class N(Command):
    reg: int


@dataclass
class R(Command):
    reg: int


@dataclass
class D(Command):
    reg: int


@dataclass
class M(Command):
    reg: int


@dataclass
class X(Command):
    reg: int
    controls: List[int]


@dataclass
class Y(Command):
    reg: int
    controls: List[int]


@dataclass
class Z(Command):
    reg: int
    controls: List[int]


@dataclass
class H(Command):
    reg: int
    controls: List[int]


@dataclass
class S(Command):
    reg: int
    controls: List[int]


@dataclass
class T(Command):
    reg: int
    controls: List[int]


@dataclass
class Rot(Command):
    angle: float
    reg: int
    controls: List[int]


@dataclass
class CRot(Command):
    angle: float
    reg: int
    controls: List[int]


@dataclass
class Diag(Command):
    a: float
    b: float
    reg: int
    controls: List[int]


@dataclass
class TInv(Command):
    reg: int
    controls: List[int]


@dataclass
class SInv(Command):
    reg: int
    controls: List[int]


@dataclass
class CNOT(Command):
    target: int
    control: int
    controls: List[int]


@dataclass
class Toffoli(Command):
    a: int
    b: int
    c: int
    controls: List[int]


@dataclass
class CZ(Command):
    target: int
    control: int
    controls: List[int]


@dataclass
class CY(Command):
    target: int
    control: int
    controls: List[int]


@dataclass
class Result:
    data: Union[int, None] = None


class ParseError(Exception):
    def __init__(self, message: str):
        super().__init__(message)


def parse_bit(bit_str: str) -> bool:
    if bit_str == '0':
        return False
    elif bit_str == '1':
        return True
    else:
        raise ParseError('%s is not a bit, must be 0 or 1' % bit_str)
    

def parse_nat(nat_str: int) -> int:
    try:
        return int(nat_str)
    except:
        raise ParseError('%s is not a natural number' % nat_str)


def parse_command(command: str) -> Result:
    argv = command.split(' ')
    argc = len(argv)
    op = argv[0]
    args = argv[1:]
    num_args = len(args)

    match op:
        case 'Q':
            if num_args == 0:
                raise ParseError('Command Q requires an argument')
            if num_args > 2:
                raise ParseError('Command Q requires at most two arguments')
            if num_args == 1:
                return Q(parse_nat(args[0]))
            return Q(parse_nat(args[1]), parse_bit(args[0]))

        case 'B':
            if num_args == 0:
                raise ParseError('Command B requires an argument')
            if num_args > 2:
                raise ParseError('Command B requires at most two arguments')
            if num_args == 1:
                return B(parse_nat(args[0]))
            return B(parse_nat(args[1]), parse_bit(args[0]))
        
        case 'N':
            if num_args != 1:
                raise ParseError('Command N requires exactly one argument')
            return N(parse_nat(args[0]))
        
        case 'M':
            if num_args != 1:
                raise ParseError('Command M requires exactly one argument')
            return M(parse_nat(args[0]))
        
        case 'R':
            if num_args != 1:
                raise ParseError('Command R requires exactly one argument')
            return R(parse_nat(args[0]))
        
        case 'quit':
            return Quit()
        
        case 'dump':
            return Dump()
        
        case 'help':
            return Help()
        
        case 'reset':
            return Reset()
        
        case 'fresh':
            return Fresh()