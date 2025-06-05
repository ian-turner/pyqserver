from abc import ABC
from typing import List, Type
from dataclasses import dataclass, is_dataclass


class Command(ABC):
    def __init_subclass__(cls: Type, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_dataclass(cls):
            dataclass(cls)

class Help(Command):
    """Displays help message"""

class Empty(Command):
    """Does nothing"""

class Reset(Command):
    """Resets the state of the quantum simulator"""

class Fresh(Command):
    """Returns the address of a free quantum register"""

class Quit(Command):
    """Quits the simulator"""

class Dump(Command):
    """Returns the current state of the simulator"""

class Protocol(Command):
    """Used for negotiation of protocol versions"""
    protocol: int

class Q(Command):
    reg: int
    bvalue: bool = False

class B(Command):
    reg: int
    bvalue: bool = False

class N(Command):
    reg: int

class R(Command):
    reg: int

class D(Command):
    reg: int

class M(Command):
    reg: int

class X(Command):
    reg: int
    controls: List[int]

class Y(Command):
    reg: int
    controls: List[int]

class Z(Command):
    reg: int
    controls: List[int]

class H(Command):
    reg: int
    controls: List[int]

class S(Command):
    reg: int
    controls: List[int]

class T(Command):
    reg: int
    controls: List[int]

class TInv(Command):
    reg: int
    controls: List[int]

class SInv(Command):
    reg: int
    controls: List[int]

class Rot(Command):
    angle: float
    reg: int
    controls: List[int]

class Diag(Command):
    a: float
    b: float
    reg: int
    controls: List[int]

class CNOT(Command):
    x: int
    y: int
    controls: List[int]

class CRot(Command):
    angle: float
    x: int
    y: int
    controls: List[int]

class Toffoli(Command):
    x: int
    y: int
    z: int
    controls: List[int]

class CZ(Command):
    x: int
    y: int
    controls: List[int]

class CY(Command):
    x: int
    y: int
    controls: List[int]


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
    

def parse_nats(float_strs: List[str]) -> List[float]:
    return [parse_nat(x) for x in float_strs]


def parse_command(command_str: str) -> Command:
    if command_str[0] == '#':
        # ignoring comments
        return Empty()
    
    # splitting command into words
    command_str_split = command_str.split(' ')
    op = command_str_split[0]
    args = command_str_split[1:]

    # parsing command into operation
    match op, args:
        case 'Q', [reg]: return Q(parse_nat(reg))
        case 'Q', [reg, bit]: return Q(parse_nat(reg), parse_bit(bit))
        case 'Q', []: raise ParseError('Command Q requires an argument')
        case 'Q', [*_]: raise ParseError('Command Q requires at most two arguments')
        case 'B', [reg]: return B(parse_nat(reg))
        case 'B', [reg, bit]: return B(parse_nat(reg), parse_bit(bit))
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
        case 'X', [reg, *ctrls]: return X(parse_nat(reg), parse_nats(ctrls))
        case 'X', []: raise ParseError('Command X requires at least one argument')
        case 'Y', [reg, *ctrls]: return Y(parse_nat(reg), parse_nats(ctrls))
        case 'Y', []: raise ParseError('Command Y requires at least one argument')
        case 'Z', [reg, *ctrls]: return Z(parse_nat(reg), parse_nats(ctrls))
        case 'Z', []: raise ParseError('Command Z requires at least one argument')
        case 'H', [reg, *ctrls]: return H(parse_nat(reg), parse_nats(ctrls))
        case 'H', []: raise ParseError('Command H requires at least one argument')
        case 'S', [reg, *ctrls]: return S(parse_nat(reg), parse_nats(ctrls))
        case 'S', []: raise ParseError('Command S requires at least one argument')
        case 'T', [reg, *ctrls]: return T(parse_nat(reg), parse_nats(ctrls))
        case 'T', []: raise ParseError('Command T requires at least one argument')
        case 'T*', [reg, *ctrls]: return TInv(parse_nat(reg), parse_nats(ctrls))
        case 'T*', []: raise ParseError('Command T* requires at least one argument')
        case 'S*', [reg, *ctrls]: return SInv(parse_nat(reg), parse_nats(ctrls))
        case 'S*', []: raise ParseError('Command S* requires at least one argument')
        case 'DIAG', [reg, *ctrls, a, b]: return Diag(parse_nat(reg), parse_nats(ctrls), \
            parse_float(a), parse_float(b))
        case 'DIAG', [*_]: raise ParseError('Command DIAG requires at least three arguments')
        case 'ROT', [r, reg, *ctrls]: return Rot(parse_float(r), parse_nat(reg), \
            parse_nats(ctrls))
        case 'ROT', [*_]: raise ParseError('Command ROT requires at least two arguments')
        case 'CROT', [r, x, y, *ctrls]: return CRot(parse_float(r), parse_nat(x), \
            parse_nat(y), parse_nats(ctrls))
        case 'CROT', [*_]: raise ParseError('Command CROT requires at least three arguments')
        case 'CNOT', [x, y, *ctrls]: return CNOT(parse_nat(x), parse_nat(y), \
            parse_nats(ctrls))
        case 'CNOT', [*_]: raise ParseError('Command CNOT requires at least two arguments')
        case 'TOF', [a, b, c, *ctrls]: return Toffoli(parse_nat(a), \
            parse_nat(b), parse_nat(c), parse_nats(ctrls))
        case 'TOF', [*_]: raise ParseError('Command TOF requires at least three arguments')
        case 'CZ', [x, y, *ctrls]: return CZ(parse_nat(x), parse_nat(y), parse_nats(ctrls))
        case 'CZ', [*_]: raise ParseError('Command CZ requires at least two arguments')
        case 'CY', [x, y, *ctrls]: return CY(parse_nat(x), parse_nat(y), parse_nats(ctrls))
        case 'CY', [*_]: raise ParseError('Command CY requires at least two arguments')
        case 'dump', _: return Dump()
        case 'fresh', _: return Fresh()
        case 'reset', _: return Reset()
        case 'help', _: return Help()
        case 'quit', _: return Quit()
        case _, _: raise ParseError('Unrecognized operation')