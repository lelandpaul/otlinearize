#! /usr/bin/python

"""

Provides the LinConstraint class.


LinConstraints are callables that evaluate input-output pairs and return a
non-negative integer.

For efficiency, they precompute a precset: a list of 2-tuples of sets such that
a violation is scored if something in precset[1] precedes something in
precset[0]. The class maintains an internal dictionary of {input: precset};
when a new input is encountered, the precset is calculated.

Calculating a precset involves:
	- an iterator that selects particular parts of an input to consider
	- a filter that reduces this set
	- a reducer that takes the set and creates precsets

To implement a specific constraint, subclass LinConstraint and override those
three attributes.

"""


class LinConstraint:

	def __init__(self):
		pass

	def iterator(self, tree):
		# iterates over elements of a tree. To be defined in the subclass.
		pass

	def filter(self,tree_iter):
		# filters iterated elements. To be defined in the subclass.
		pass

	def reduce(self,tree_filter):
		# reduces filtered elements to a precset. To be defined in the
		# subclass.
		pass


	def build_precset(self,inp):
		# given an input, creates a precset.
		pass

	def __call__(self,inp,out):
		# (inp,out) -> int
		pass

	def __getitem__(self,inp):
		# return the precset
		pass





