import os
import sys
import pytest

from simulator import Simulator


# adding the directory ../src to sys.path
sys.path.append(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'src'))


@pytest.fixture
def sim():
    """Set up test simulator"""
    sim = Simulator(verbose=True, lazy=False)
    yield sim


def test_new_qubit(sim):
    """Testing qubit creation"""