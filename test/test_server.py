import pytest
import socket

SERVER_PORT = 1901


def run_test_script(client, filename):
    with open(filename, 'r') as f:
        lines = [x.strip() + '\n' for x in f.readlines()]
        for line in lines:
            client.send(line.encode())


@pytest.fixture
def client():
    """Set up a test socket client"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('127.0.0.1', SERVER_PORT))
        yield client
        client.close()


def test_connection(client):
    """Testing connection to qserver"""
    resp = client.recv(1024)
    assert resp == b'# quantum server, version 0.2.\n'
    client.send(b'Universal\nquit\n')


def test_init_commands(client):
    """Testing basic bit/qubit initialization operations"""
    run_test_script(client, 'test/basic.txt')