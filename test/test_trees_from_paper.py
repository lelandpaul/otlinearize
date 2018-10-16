#! /usr/python

import pytest
from bin import *


# Load trees
@pytest.fixture(params = ["BaseGenSpec",
						  "MovedSpec",
						  "RollUpHead",
						  "RollUpHeadEmpty",])
def tree(request):
	t = mtree.parseTreeFile('trees/paper/' + request.param + '.txt')
	return(t)

# Test that trees have been loaded correctly

@pytest.mark.parametrize("result_dict", [
	{ "BaseGenSpec": "[A2 [C1 C0 ] [A1 [B1 B0 ] A0 ] ]",
	  "MovedSpec":   "[A2 [C1 C0 ] [A1 [B1 [C1 C0 ] B0 ] A0 ] ]",
	  "RollUpHead": "[A1 [B1 [C1 C0 ] [B C0 B0 ] ] [A [B C0 B0 ] A0 ] ]",
	  "RollUpHeadEmpty": "[A1 [B1 [E1 [C1 C0 ] [E C0 E0 ] ] [B [E C0 E0 ] B0 ] ] [A [B [E C0 E0 ] B0 ] A0 ] ]"
	}])
def test_tree_bracket_string(tree, result_dict):
	assert tree.bracket_string == result_dict[tree.name]
