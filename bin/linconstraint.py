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

	def __init__(self,name="LinCon"):
		self.precsets = dict() # dictionary from inp to precset
		self.name = name

	def __call__(self,inp,out):
		# (inp,out) -> int
		precset = self.get_precset(inp)
		# Map each prec to either 1 or 0 based on the output
		violations = list(map(lambda x: self.check_viol(x,out),
							  precset))
		# Reduce and return
		return(sum(violations))
			

	def __getitem__(self,inp):
		# return the precset
		return(self.get_precset(inp))

	def __repr__(self):
		return(self.name)

	def build_precset(self,inp):
		# given an input, creates a precset.
		targets = [i for i in self.iterator(inp) if self.filter(i,inp)]
		precset = list(map(self.reduce,targets))
		precset = tuple(map(self.stringify,precset))
		return(precset)

	def stringify(self,prec):
		# takes a tuple of sets of nodes, returns a tuple of sets of strings
		return(tuple(map(lambda y: set(map(lambda x: str(x).lower(),y)),prec)))

	def get_precset(self,inp):
		# given an input, returns the precset (creating it if necessary)

		if inp not in self.precsets:
			self.precsets[inp] = self.build_precset(inp)
		return(self.precsets[inp])

	def prec_pairs(self,string):
		# given a string, yields all pairs (a,b) where a < b
		for i in range(len(string)-1):
			for j in range(i+1,len(string)):
				yield((string[i],string[j]))

	def check_viol(self,precset,out):
		# Given a particular precset and an output, check if a violation is
		# accrued.
		for pair in self.prec_pairs(out):
			if pair[0] in precset[1] and pair[1] in precset[0]:
				return(1)
		return(0)

	# The next three are to be defined in the subclasses.

	def iterator(self, tree):
		# iterates over elements of a tree. To be defined in the subclass.
		pass

	def filter(self,tree_iter,inp):
		# Boolean: filters iterated elements. To be defined in the subclass.
		pass

	def reduce(self,tree_filter):
		# reduces filtered elements to a precset. To be defined in the
		# subclass.
		pass




