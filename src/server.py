import socket
from threading import Thread

from parser import *


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

    def _handle_connection(self, conn, addr):
        print('Connected to %s' % str(addr))
        self.num_conns += 1
        with conn:
            # sending initial info message
            connFile = conn.makefile(mode='rw')
            connFile.write('# quantum server, version 0.2.\n')

            # reading simulation mode from client
            sim_mode = connFile.readline().strip()
            
            # making sure only universal mode is selected
            if sim_mode != 'Universal':
                connFile.write('Invalid simulation method\n')

            # parsing commands line by line
            while True:
                # reading the next line
                line = connFile.readline()
                if not line:
                    break

                # parsing the line
                command_raw = line.strip()
                command = parse_command(command_raw)
                print(command)

        print('Connection to %s closed' % str(addr))
        self.num_conns -= 1