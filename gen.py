#! /usr/bin/python


"""

Provides the Gen class, along with functions for iterating over output
linearizations given a particular tree input.


"""


from itertools import permutations

def gen_strings(tree, null_phon = {}, spaces = False):
	null_phon = {t.lower() for t in null_phon}
	terminals = {t.label[0].lower() for t in tree.terminals}
	terminals = terminals - null_phon # remove silent things
	for perm in permutations(terminals):
		yield ''.join(perm)


class Gen:

	def __init__(self, function = gen_strings):
		self.function = gen_strings
		self.dictionary = dict()

	def __call__(self, inp):
		# yield the precreated values in the dictionary
		# otherwise, build them and then yield them
		yield from self.dictionary.get(inp, list(self.function(inp)))

	def __getitem__(self, inp):
		yield from self.dictionary[inp]
