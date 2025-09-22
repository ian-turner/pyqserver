import sys
import socket
from threading import Thread

from .parser import *
from .simulator import *
from .cirq_simulator import CirqSimulator
from .qiskit_simulator import QiskitSimulator


class Server:
    def __init__(self,
                 port: int,
                 max_conns: int,
                 verbose: bool = False,
                 sim_method: str = 'cirq',
                 debug: bool = True):
        self.port = port
        self.max_conns = max_conns
        self.verbose = verbose
        self.num_conns = 0
        self.sim_method = sim_method
        self.debug = debug

    def run(self):
        # setting up socket connection
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                print('Starting quantum server on port %d with max %d connections' % \
                        (self.port, self.max_conns))
                s.bind(('127.0.0.1', self.port))
                s.listen()

                # waiting for new connections and handling
                try:
                    while True:
                        # handling connection
                        conn, addr = s.accept()
                        while self.num_conns >= self.max_conns:
                            # stopping at connection limit and waiting
                            pass

                        t = Thread(target=self._handle_connection, args=(conn, addr,))
                        t.start()
                except KeyboardInterrupt:
                    print('\nShutting down quantum server')

    def _get_simulator(self):
        if self.sim_method == 'qiskit':
            return QiskitSimulator()
        elif self.sim_method == 'cirq':
            return CirqSimulator()

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
                while sim_mode != 'Universal':
                    conn.send(b'Invalid simulation method\n')
                    sim_mode = connFile.readline().strip()

                # parsing commands line by line
                simulator = self._get_simulator()
                while True:
                    # reading the next line
                    line = connFile.readline()
                    if not line: break

                    try:
                        # parsing the command
                        command_str: str = line.strip()
                        if self.verbose:
                            print('\tIncoming command: "%s"' % command_str)

                        command: Command = parse_command(command_str)
                        if self.verbose:
                            print('\tParsed command: %s' % command)

                        # interpreting the command
                        result: Result = simulator.execute(command)
                        if self.verbose:
                            print('\tSimulator result: %s' % result)

                        # handling simulator result
                        match result:
                            case OK():
                                pass
                            case Null():
                                pass
                            case Terminate():
                                break
                            case Reply():
                                conn.send(('Reply "%s"\n' % result.message).encode())
                            case Info():
                                conn.send(result.content.encode())

                    # handling errors
                    except ParseError as e:
                        print('Parse error: %s' % str(e))
                        conn.send(('! Parse error: %s. Try help.\n' % str(e)).encode())
                    except UsageError as e:
                        print('Usage error: %s' % str(e))
                        conn.send((('Usage error "! %s"\n' % str(e))).encode())
                    except Exception as e:
                        if self.debug:
                            raise e
                        print('Internal error: %s' % str(e))
                        conn.send(('Internal error: %s\n' % str(e)).encode())

        except ConnectionResetError:
            print('Error: connection to %s reset' % str(addr), file=sys.stderr)

        print('Connection to %s closed' % str(addr))
        self.num_conns -= 1
