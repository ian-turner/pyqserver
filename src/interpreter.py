from abc import ABC
from dataclasses import dataclass, is_dataclass

from parser import *
from simulator import *


HELP_MESSAGE = """
Control commands:
help                - print usage information
reset               - reset the machine to the initial state
quit                - quit
fresh               - return the address of a free register

QRAM commands:
Q x                 - initialize qubit x to |0>
Q x b               - initialize qubit x to |b>
B x                 - initialize bit x to 0
B x b               - initialize bit x to b
N x                 - initialize qubit from bit x
M x                 - measure qubit x into bit x
D x                 - discard bit or qubit x
R x                 - read and discard bit or qubit x

Gate operations:
X x [ctrls]         - apply X-gate to qubit x
Y x [ctrls]         - apply Y-gate to qubit x
Z x [ctrls]         - apply Y-gate to qubit x
H x [ctrls]         - apply H-gate to qubit x
S x [ctrls]         - apply S-gate to qubit x
S* x [ctrls]        - apply S*-gate to qubit x
T x [ctrls]         - apply T-gate to qubit x
T* x [ctrls]        - apply T*-gate to qubit x
CNOT x y [ctrls]    - apply CNOT gate to qubits x and y
TOF x y z [ctrls]   - apply Toffoli gate to qubits x, y, and z
CZ x y [ctrls]      - apply controlled-Z gate to qubits x and y
CY x y [ctrls]      - apply controlled-Y gate to qubits x and y
DIAG a b x [ctrls]  - apply diagonal gate with values a, b to qubit x
ROT r x [ctrls]     - apply RZ gate with angle r to qubit x
CROT r x y [ctrls]  - apply controlled-RZ gate with angle r to qubits x and y
"""


class Response(ABC):
    def __init_subclass__(cls: Type, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_dataclass(cls):
            dataclass(cls)


class Reply(Response):
    message: str

class Info(Response):
    content: str

class OK(Response):
    pass

class Terminate(Response):
    pass

class Null(Response):
    pass


def interpret_command(command: Command, simulator: Simulator, verbose: bool = False) -> Response:
    match command:
        case Empty(): return Null()
        case Quit(): return Terminate()
        case Help(): return Info(HELP_MESSAGE)
        case Dump(): return Info(simulator.dump())
        case Reset():
            simulator.reset()
            return OK()
        case Fresh():
            pass
        case Q():
            simulator.new_qubit(command.reg, command.bvalue)
            return OK()
        case B():
            pass
        case N():
            pass
        case R():
            pass
        case D():
            pass
        case M():
            pass
        case X():
            pass
        case Y():
            pass
        case Z():
            pass
        case H():
            pass
        case S():
            pass
        case SInv():
            pass
        case T():
            pass
        case TInv():
            pass
        case Rot():
            pass
        case Diag():
            pass
        case CNOT():
            pass
        case CRot():
            pass
        case Toffoli():
            pass
        case CZ():
            pass
        case CY():
            pass