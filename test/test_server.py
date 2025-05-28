import pytest
import socket

SERVER_PORT = 1901


@pytest.fixture
def client():
    """Set up a test socket client"""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        yield client


@pytest.mark.order(1)
def test_connection(client):
    """Testing connection to qserver"""
    client.connect(('127.0.0.1', SERVER_PORT))
    client.send(b'Universal\nquit\n')
    client.close()