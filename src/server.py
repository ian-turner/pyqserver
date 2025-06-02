import socket
from multiprocessing import Process

from simulator import *


def parse_command(command: str) -> SimOp:
    print(command)


def handle_connection(conn):
    try:
        conn.send('# quantum server, version 0.2.\n'.encode())
        # reading simulation mode from client
        connFile = conn.makefile()
        sim_mode = connFile.readline().strip()
        match sim_mode:
            case 'Universal':
                # setting up simulator
                sim = Simulator()

                while True:
                    # reading the next line
                    line = connFile.readline()
                    if not line:
                        connFile.close()
                        conn.close()
                        break

                    # processing 'quit' condition
                    command = line.strip()
                    match command:
                        case 'quit':
                            connFile.close()
                            conn.close()
                            break
                        case 'reset':
                            sim.reset()
                        case _:
                            # parsing command into simulator operations
                            operation = parse_command(command)
                            result = sim.execute(operation)
                            if result != None:
                                conn.send(('Reply "%d"\n' % result).encode())
                    
            case _:
                conn.send(b'Invalid simulation method\n')
                
    except Exception as e:
        conn.send(b'Internal error: %s\n' % e)


def socket_worker(sock):
    """Handles socket connections in parallel"""
    while True:
        # waiting for a new connection
        conn, addr = sock.accept()
        print('Connected to %s' % str(addr))
        handle_connection(conn)
        print('Connection to %s closed' % str(addr))


class Server:
    def __init__(self, port: int, num_workers: int, verbose: bool = False):
        self.port = port
        self.num_workers = num_workers
        self.verbose = verbose

    def run(self):
        # setting up socket connection
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            print('Starting quantum server on port %d with %d workers' % \
                  (self.port, self.num_workers))
            s.bind(('127.0.0.1', self.port))
            s.listen()
            
            # starting worker processes to listen for connections
            procs = [Process(target=socket_worker, args=(s,)) \
                    for _ in range(self.num_workers)]
            for p in procs:
                p.start()

            # waiting for processes to finish
            for p in procs:
                p.join()