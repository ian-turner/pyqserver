import sys
import socket
from threading import Thread

from parser import *


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


class Server:
    def __init__(self, port: int, max_conns: int, verbose: bool = False):
        self.port = port
        self.max_conns = max_conns
        self.verbose = verbose
        self.num_conns = 0

    def run(self):
        # setting up socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('Starting quantum server on port %d with max %d connections' % \
                    (self.port, self.max_conns))
            s.bind(('127.0.0.1', self.port))
            s.listen()

            # waiting for new connections and handling
            while True:
                # handling connection
                conn, addr = s.accept()
                if self.num_conns < self.max_conns:
                    t = Thread(target=self._handle_connection, args=(conn, addr,))
                    t.start()
                else:
                    conn.send(b'Internal error: Too many conncurrent connections\n')
                    conn.close()

    def _handle_connection(self, conn, addr):
        self.num_conns += 1
        try:
            print('Connected to %s' % str(addr))
            with conn:
                # sending initial info message
                conn.send(b'# quantum server, version 0.2.\n')

                # reading simulation mode from client
                connFile = conn.makefile()
                sim_mode = connFile.readline().strip()
                
                # making sure only universal mode is selected
                if sim_mode != 'Universal':
                    conn.send(b'Invalid simulation method\n')

                # parsing commands line by line
                while True:
                    # reading the next line
                    line = connFile.readline()
                    if not line:
                        break

                    # parsing the command
                    command_raw = line.strip()
                    try:
                        command = parse_command(command_raw)
                        print(command)
                        match command:
                            case Quit():
                                break
                            case Help():
                                conn.send(HELP_MESSAGE.encode())

                    except ParseError as e:
                        conn.send(('! Parse error: %s. Try help.\n' % str(e)).encode())

            print('Connection to %s closed' % str(addr))

        except ConnectionResetError:
            print('Error: connection to %s reset' % str(addr), file=sys.stderr)

        self.num_conns -= 1