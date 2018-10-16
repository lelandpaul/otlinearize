#! /usr/python

import pytest
from bin.mtree import *


@pytest.fixture
def terminal_a():
	return(TerminalNode('A'))

def test_terminal_node_label(terminal_a):
	assert terminal_a.label == ('A',0)

def test_terminal_node_repr(terminal_a):
	assert str(terminal_a) == 'A0'


