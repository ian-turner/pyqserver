import socket
from multiprocessing import Process
from argparse import ArgumentParser


# server config
HOST = '127.0.0.1'
DEFAULT_PORT = 1901
DEFAULT_NUM_WORKERS = 30


def socket_worker(socket):
    """Handles socket connections in parallel"""
    while True:
        # waiting for a new connection
        conn, addr = socket.accept()
        connFile = conn.makefile()
        with conn:
            print('Connected to %s' % str(addr))
            conn.send('# quantum server, version 0.1.\n'.encode())
            while True:
                # reading input from client line by line
                line = connFile.readline()
                if not line:
                    connFile.close()
                    conn.close()
                    break
                print(line, end='')


if __name__ == '__main__':
    # reading command line arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=DEFAULT_PORT)
    parser.add_argument('-n', '--num_workers', type=int, default=DEFAULT_NUM_WORKERS)
    args = parser.parse_args()

    # setting up socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Starting quantum server on port %d with %d workers' % (args.port, args.num_workers))
        s.bind((HOST, args.port))
        s.listen()
        
        # starting worker processes to listen for connections
        procs = [Process(target=socket_worker, args=(s,)) \
                 for _ in range(args.num_workers)]
        for p in procs:
            p.start()

        for p in procs:
            p.join()