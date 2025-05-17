import socket
from multiprocessing import Process


# server config
HOST = '127.0.0.1'
PORT = 1901
NUM_WORKERS = 20


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
    # setting up socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Starting quantum server')
        s.bind((HOST, PORT))
        s.listen()
        
        # starting worker processes to listen for connections
        procs = [Process(target=socket_worker, args=(s,)) for _ in range(NUM_WORKERS)]
        for p in procs:
            p.start()

        for p in procs:
            p.join()