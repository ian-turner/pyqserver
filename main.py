import socket
from multiprocessing import Process
from argparse import ArgumentParser


def socket_worker(socket):
    """Handles socket connections in parallel"""
    while True:
        # waiting for a new connection
        conn, addr = socket.accept()
        connFile = conn.makefile()
        with conn:
            print('Connected to %s' % str(addr))
            conn.send('# quantum server, version 0.2.\n'.encode())
            # reading simulation mode from client
            sim_mode = connFile.readline().strip()
            if sim_mode == 'Universal':
                # reading commands
                while True:
                    line = connFile.readline()
                    if not line:
                        connFile.close()
                        conn.close()
                        break
                    command = line.strip()
                    if command == 'quit':
                        connFile.close()
                        conn.close()
                        break
                    
                    # parsing command
                    print(command)
                    # ...
            else:
                raise Exception('Invalid simulation mode')


if __name__ == '__main__':
    # reading command line arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=1901)
    parser.add_argument('-n', '--num_workers', type=int, default=30)
    args = parser.parse_args()

    # setting up socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Starting quantum server on port %d with %d workers' % (args.port, args.num_workers))
        s.bind(('127.0.0.1', args.port))
        s.listen()
        
        # starting worker processes to listen for connections
        procs = [Process(target=socket_worker, args=(s,)) \
                 for _ in range(args.num_workers)]
        for p in procs:
            p.start()

        for p in procs:
            p.join()