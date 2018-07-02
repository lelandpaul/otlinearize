#! /usr/bin/python


"""

Provides functions for iterating over output linearizations given a particular tree
input.

"""


from itertools import permutations

def gen_strings(tree, null_phon = {}, spaces = False):
	null_phon = {t.lower() for t in null_phon}
	terminals = {t.label[0].lower() for t in tree.terminals}
	terminals = terminals - null_phon # remove silent things
	for perm in permutations(terminals):
		yield ''.join(perm)


