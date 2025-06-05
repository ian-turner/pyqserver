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
    control: int
    target: int
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
    

def parse_float(float_str: float) -> float:
    try:
        return float(float_str)
    except:
        raise ParseError('%s is not a float' % float_str)


def parse_command(command: str) -> Result:
    command_split = command.split(' ')
    op = command_split[0]
    args = command_split[1:]

    match op, args:
        case 'Q', [reg]: return Q(parse_nat(reg))
        case 'Q', [bit, reg]: return Q(parse_nat(reg), parse_bit(bit))
        case 'Q', []: raise ParseError('Command Q requires an argument')
        case 'Q', [*_]: raise ParseError('Command Q requires at most two arguments')
        case 'B', [reg]: return B(parse_nat(reg))
        case 'B', [bit, reg]: return B(parse_nat(reg), parse_bit(bit))
        case 'B', []: raise ParseError('Command B requires an argument')
        case 'B', [*_]: raise ParseError('Command B requires at most two arguments')
        case 'N', [reg]: return N(parse_nat(reg))
        case 'N', [*_]: raise ParseError('Command N requires exactly one argument')
        case 'M', [reg]: return M(parse_nat(reg))
        case 'M', [*_]: raise ParseError('Command M requires exactly one argument')
        case 'R', [reg]: return R(parse_nat(reg))
        case 'R', [*_]: raise ParseError('Command R requires exactly one argument')
        case 'D', [reg]: return D(parse_nat(reg))
        case 'D', [*_]: raise ParseError('Command D requires exactly one argument')
        case 'X', [reg, *ctrls]: return X(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'X', []: raise ParseError('Command X requires at least one argument')
        case 'Y', [reg, *ctrls]: return Y(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'Y', []: raise ParseError('Command Y requires at least one argument')
        case 'Z', [reg, *ctrls]: return Z(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'Z', []: raise ParseError('Command Z requires at least one argument')
        case 'H', [reg, *ctrls]: return H(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'H', []: raise ParseError('Command H requires at least one argument')
        case 'S', [reg, *ctrls]: return S(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'S', []: raise ParseError('Command S requires at least one argument')
        case 'T', [reg, *ctrls]: return T(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'T', []: raise ParseError('Command T requires at least one argument')
        case 'T*', [reg, *ctrls]: return TInv(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'T*', []: raise ParseError('Command T* requires at least one argument')
        case 'S*', [reg, *ctrls]: return SInv(parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'S*', []: raise ParseError('Command S* requires at least one argument')
        case 'DIAG', [a, b, reg, *ctrls]: return Diag(parse_float(a), parse_float(b), \
            parse_nat(reg), [parse_nat(x) for x in ctrls])
        case 'DIAG', [*_]: raise ParseError('Command DIAG requires at least three arguments')
        case 'ROT', [r, reg, *ctrls]: return Rot(parse_float(r), parse_nat(reg), \
            [parse_nat(x) for x in ctrls])
        case 'ROT', [*_]: raise ParseError('Command ROT requires at least two arguments')
        case 'CROT', [r, x, y, *ctrls]: return CRot(parse_float(r), parse_nat(x), \
            parse_nat(y), [parse_nat(x) for x in ctrls])
        case 'CROT', [*_]: raise ParseError('Command CROT requires at least three arguments')
        case 'CNOT', [x, y, *ctrls]: return CNOT(parse_nat(x), \
            parse_nat(y), [parse_nat(x) for x in ctrls])
        case 'CNOT', [*_]: raise ParseError('Command CNOT requires at least two arguments')
        case 'TOF', [a, b, c, *ctrls]: return Toffoli(parse_nat(a), \
            parse_nat(b), parse_nat(c), [parse_nat(x) for x in ctrls])
        case 'TOF', [*_]: raise ParseError('Command TOF requires at least three arguments')
        case 'CZ', [x, y, *ctrls]: return CZ(parse_nat(x), \
            parse_nat(y), [parse_nat(x) for x in ctrls])
        case 'CZ', [*_]: raise ParseError('Command CZ requires at least two arguments')
        case 'CY', [x, y, *ctrls]: return CY(parse_nat(x), \
            parse_nat(y), [parse_nat(x) for x in ctrls])
        case 'CY', [*_]: raise ParseError('Command CY requires at least two arguments')
        case 'dump', _: return Dump()
        case 'fresh', _: return Fresh()
        case 'reset', _: return Reset()
        case 'help', _: return Help()
        case 'quit', _: return Quit()