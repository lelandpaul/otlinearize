#! /usr/python

import pytest
from bin import *


# Load trees
@pytest.fixture
def tree_BaseGenSpec():
	t = mtree.parseTreeFile('trees/paper/BaseGenSpec.txt')
	return(t)

@pytest.fixture
def tree_MovedSpec():
	t = mtree.parseTreeFile('trees/paper/MovedSpec.txt')
	return(t)



# Test that trees have been loaded correctly

@pytest.mark.parametrize("tree, brackets", [
	(tree_BaseGenSpec(), "[A2 [C1 C0 ] [A1 [B1 B0 ] A0 ] ]"),
	(tree_MovedSpec(), "[A2 [C1 C0 ] [A1 [B1 [C1 C0 ] B0 ] A0 ] ]"),
	])
def test_tree_bracket_string(tree, brackets):
	assert tree.bracket_string == brackets
