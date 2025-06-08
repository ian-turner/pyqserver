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


class Result(ABC):
    def __init_subclass__(cls: Type, **kwargs):
        super().__init_subclass__(**kwargs)
        if not is_dataclass(cls):
            dataclass(cls)


class Reply(Result):
    """Send reply string to user"""
    message: str

class Info(Result):
    """Send message string to user (meant for debugging)"""
    content: str

class OK(Result):
    """The instruction has executed properly"""

class Terminate(Result):
    """Shut down the simulator and close the connection"""

class Null(Result):
    """Nothing happened"""


class Interpreter:
    def __init__(self, lazy: bool = False, verbose: bool = False):
        self.lazy = lazy
        self.verbose = verbose
        self.sim = Simulator(verbose=verbose)

    def interpret(self, command: Command) -> Result:
        match command:
            case Empty(): return Null()
            case Quit(): return Terminate()
            case Help(): return Info(HELP_MESSAGE)
            case Dump(): return Info(self.sim.dump())
            case Reset():
                self.sim.reset()
                return OK()
            case Fresh():
                reg: int = self.sim.fresh()
                return Reply(str(reg))
            case Q():
                self.sim.new_qubit(command.reg, command.bvalue)
                return OK()
            case B():
                self.sim.new_bit(command.reg, command.bvalue)
                return OK()
            case N():
                self.sim.new_qubit_from_bit(command.reg)
                return OK()
            case R():
                val = self.sim.read(command.reg)
                return Reply(str(val))
            case D():
                self.sim.discard(command.reg)
                return OK()
            case M():
                self.sim.measure(command.reg)
                return OK()
            case X():
                self.sim.gate_X(command.reg, command.controls)
                return OK()
            case Y():
                self.sim.gate_Y(command.reg, command.controls)
                return OK()
            case Z():
                self.sim.gate_Z(command.reg, command.controls)
                return OK()
            case H():
                self.sim.gate_H(command.reg, command.controls)
                return OK()
            case S():
                self.sim.gate_S(command.reg, command.controls)
                return OK()
            case SInv():
                self.sim.gate_SInv(command.reg, command.controls)
                return OK()
            case T():
                self.sim.gate_T(command.reg, command.controls)
                return OK()
            case TInv():
                self.sim.gate_TInv(command.reg, command.controls)
                return OK()
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