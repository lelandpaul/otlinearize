#! /usr/python

import pytest
from bin import mtree
from bin import con
from bin import tableau
from bin import gen


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



# Test that the correct contenders are selected

def test_contenders_with_two_constraints(tree):
	result_dict = {
			"BaseGenSpec": {'cba','cab'},
			"MovedSpec":   {'cba','cab'},
			"RollUpHead":  {'cba','acb'},
			"RollUpHeadEmpty": {'abc','cba'},
			"LongHeadEmpty": {'abc', 'bca'},
			}

	# Build Con:
	conlist = [ con.Antisymmetry(),
				con.HeadFinality(),
				]

	t = tableau.Tableau(tree,
						conlist,
						gen = gen.Gen(lambda x: gen.gen_strings(x, null_phon = {'E'}))
						)

	try:	# The test is going to try some trees that aren't relevant
		assert t.contenders == result_dict[tree.name]
	except KeyError:
		assert 1 == 1 # just pass



def test_contenders_with_three_constraints(tree):
	result_dict = {
			"Basic": {'acb','abc','cba'},
			"LongMovedSpec": {'dacb','dabc','dcba'},
			"HighHead": {'badc','bacd','dcba'},
			}

	# Build Con:
	conlist = [ con.Antisymmetry(),
				con.HeadFinality(),
				con.HeadFinality(alpha = 'BP'),
				]

	t = tableau.Tableau(tree,
						conlist,
						gen = gen.Gen(lambda x: gen.gen_strings(x, null_phon = {'E'}))
						)

	try:	# The test is going to try some trees that aren't relevant
		assert t.contenders == result_dict[tree.name]
	except KeyError:
		assert 1 == 1 # just pass


def test_contenders_ComplexMovedSpec(tree):
	# This one needs a different HeadFinality-Alpha
	result_dict = {
			"ComplexMovedSpec": {'dcab','cdab','dcba'},
			}

	# Build Con:
	conlist = [ con.Antisymmetry(),
				con.HeadFinality(),
				con.HeadFinality(alpha = 'CP'),
				]

	t = tableau.Tableau(tree,
						conlist,
						gen = gen.Gen(lambda x: gen.gen_strings(x, null_phon = {'E'}))
						)

	try:	# The test is going to try some trees that aren't relevant
		assert t.contenders == result_dict[tree.name]
	except KeyError:
		assert 1 == 1 # just pass

