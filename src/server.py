import sys
import socket
from threading import Thread

from parser import *
from interpreter import *
from simulator import *


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
                while self.num_conns >= self.max_conns:
                    # stopping at connection limit and waiting
                    pass

                t = Thread(target=self._handle_connection, args=(conn, addr,))
                t.start()

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
                interpreter = Interpreter()
                while True:
                    # reading the next line
                    line = connFile.readline()
                    if not line: break

                    try:
                        # parsing the command
                        command_str: str = line.strip()
                        command: Command = parse_command(command_str)

                        # interpreting the command
                        result: Result = interpreter.interpret(command)
                        
                        if self.verbose:
                            print('\tIncoming command: "%s"' % command_str)
                            print('\tParsed command: %s' % command)
                            print('\tInterpreter result: %s' % result)

                        # handling interpreter result
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
                        print('Internal error: %s' % str(e))
                        conn.send((('Usage error "! %s"\n' % str(e))).encode())
                    except Exception as e:
                        print('Internal error: %s' % str(e))
                        conn.send(('Internal error: %s\n' % str(e)).encode())

        except ConnectionResetError:
            print('Error: connection to %s reset' % str(addr), file=sys.stderr)

        print('Connection to %s closed' % str(addr))
        self.num_conns -= 1