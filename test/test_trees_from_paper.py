#! /usr/python

import pytest
from bin import *


# Load trees

@pytest.fixture(params = ["Basic",
						  "BaseGenSpec",
						  "MovedSpec",
						  "RollUpHead",
						  "RollUpHeadEmpty",
						  "LongHeadEmpty",
						  "LongMovedSpec",
						  "HighHead",
						  "ComplexMovedSpec",])
def tree(request):
	t = mtree.parseTreeFile('trees/paper/' + request.param + '.txt')
	return(t)




# Test that trees have been loaded correctly

def test_tree_bracket_string(tree):
	result_dict = { 
	  "Basic": "[A1 [B1 [C1 C0 ] B0 ] A0 ]",
	  "BaseGenSpec": "[A2 [C1 C0 ] [A1 [B1 B0 ] A0 ] ]",
	  "MovedSpec":   "[A2 [C1 C0 ] [A1 [B1 [C1 C0 ] B0 ] A0 ] ]",
	  "RollUpHead": "[A1 [B1 [C1 C0 ] [B C0 B0 ] ] [A [B C0 B0 ] A0 ] ]",
	  "RollUpHeadEmpty": "[A1 [B1 [E1 [C1 C0 ] [E C0 E0 ] ] [B [E C0 E0 ] B0 ] ] [A [B [E C0 E0 ] B0 ] A0 ] ]",
	  "LongHeadEmpty": "[E1 [A2 [B1 B0 ] [A1 [C1 C0 ] A0 ] ] [E A0 E0 ] ]",
	  "LongMovedSpec": "[A2 [D1 D0 ] [A1 [B1 [C1 [D1 D0 ] C0 ] B0 ] A0 ] ]",
	  "HighHead": "[A1 [B1 [C1 [D1 D0 ] C0 ] B0 ] [A B0 A0 ] ]",
	  "ComplexMovedSpec": "[A2 [C1 [D1 D0 ] C0 ] [A1 [B1 [C1 [D1 D0 ] C0 ] B0 ] A0 ] ]",
	}
	assert tree.bracket_string == result_dict[tree.name]


