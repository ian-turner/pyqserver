import pytest
import socket

SERVER_PORT = 1901


@pytest.fixture
def client():
    """Set up a test socket client"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('127.0.0.1', SERVER_PORT))
        yield client
        client.close()


def test_connection(client):
    """Testing connection to qserver"""
    client.send(b'Universal\nquit\n')


def test_init_commands(client):
    """Testing basic bit/qubit initialization operations"""
    with open('test/inits.txt', 'r') as f:
        lines = [x.strip() + '\n' for x in f.readlines()]
        for line in lines:
            client.send(line.encode())