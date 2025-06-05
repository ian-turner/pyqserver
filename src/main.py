from argparse import ArgumentParser

from server import Server


if __name__ == '__main__':
    # reading command line arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=1901)
    parser.add_argument('-n', '--max_connections', type=int, default=30)
    parser.add_argument('-v', '--verbose', action='store_true')
    args = parser.parse_args()

    # starting server
    Server(args.port, args.max_connections, args.verbose).run()