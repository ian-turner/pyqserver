from argparse import ArgumentParser

from .server import Server


def main():
    # reading command line arguments
    parser = ArgumentParser()
    parser.add_argument('-p', '--port', type=int, default=1901)
    parser.add_argument('-n', '--max_connections', type=int, default=30)
    parser.add_argument('-v', '--verbose', action='store_true')
    parser.add_argument('-q', '--queueing', action='store_true')
    parser.add_argument('-g', '--gpu', action='store_true')
    parser.add_argument('-s', '--sim_method', type=str, default='cirq')
    args = parser.parse_args()

    # starting server
    Server(
        args.port,
        args.max_connections,
        args.verbose,
        sim_method=args.sim_method,
        queueing=args.queueing,
        gpu=args.gpu,
    ).run()


if __name__ == '__main__':
    main()
