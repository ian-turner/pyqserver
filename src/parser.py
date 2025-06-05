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
    command_split = command.split(' ')
    op = command_split[0]
    args = command_split[1:]

    match op, args:
        # 'Q' command
        case 'Q', [reg]: return Q(parse_nat(reg))
        case 'Q', [bit, reg]: return Q(parse_nat(reg), parse_bit(bit))
        case 'Q', []: raise ParseError('Command Q requires an argument')
        case 'Q', [*_]: raise ParseError('Command Q requires at most two arguments')

        # 'B' command
        case 'B', [reg]: return B(parse_nat(reg))
        case 'B', [bit, reg]: return B(parse_nat(reg), parse_bit(bit))
        case 'B', []: raise ParseError('Command B requires an argument')
        case 'B', [*_]: raise ParseError('Command B requires at most two arguments')

        # 'N' command
        case 'N', [reg]: return N(parse_nat(reg))
        case 'N', [*_]: raise ParseError('Command N requires exactly one argument')

        # 'M' command
        case 'M', [reg]: return M(parse_nat(reg))
        case 'M', [*_]: raise ParseError('Command M requires exactly one argument')

        # 'R' command
        case 'R', [reg]: return R(parse_nat(reg))
        case 'R', [*_]: raise ParseError('Command R requires exactly one argument')

        # 'D' command
        case 'D', [reg]: return D(parse_nat(reg))
        case 'D', [*_]: raise ParseError('Command D requires exactly one argument')

        # 'quit' command
        case 'quit', _: return Quit()