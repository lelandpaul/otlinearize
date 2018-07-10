#! /usr/bin/python

"""

Provides the Optimal Linearization constraints. These are subclasses of
LinConstraint, a callable that evaluates input/output pairs.

"""

from linconstraint import LinConstraint
from itertools import product


class Antisymmetry(LinConstraint):
	"""
	Enforces the Antisymmetry constraint: maps asymmetric c-command &
	path-command between heads to precedence.
	"""

	def __init__(self,name="Antisymmetry"):
		super().__init__(name) # pass the name into the superclass

	def iterator(self, tree):
		# Iterate over pairs of words and terminals
		yield from product(tree.words,tree.terminals)

	def filter(self,pair,tree):
		# Filter: return true for pairs of (word, terminal) where the word
		# c-commands the terminal (and not vice versa) and also where the word
		# path-commands the terminal.
		return(pair[0].path_commands(pair[1]) and
			pair[0].ccommand(pair[1]) and not pair[1].ccommand(pair[0]))

	def reduce(self,pair):
		# Make a prec: take the set of terminals dominated by the word and set
		# them to precede the terminal.
		preceders = set(pair[0].terminals_dominated)
		followers = {pair[1]}
		return((preceders,followers))


class HeadFinality(LinConstraint):
	"""
	Enforces the HeadFinality constraint: For each branching node, those things
	path commanded by the node and dominated by its head should follow those
	things path-commanded by the node and dominated by its child.
	"""

	def __init__(self,name="HeadFinality",alpha = None):
		# This one needs to do something funny to account for the alpha
		if not alpha:
			super().__init__(name) # pass on the name as is
			self.alpha = lambda x: x.root # a function to grab the root
		else:
			super().__init__(name + '-' + alpha) # there was an explicit alpha
			self.alpha = lambda x: x[alpha] # function to graph alpha node

	def iterator(self, tree):
		# iterate over branching nodes
		yield from tree.branching_nodes

	def filter(self,node,tree):
		# return true only for those nodes dominated by alpha
		alpha = self.alpha(tree)
		return(alpha.dominates(node))

	def reduce(self,node):
		# make a prec: 
		# terminals dominated by the head and path-commanded by node <
		# terminals dominated by the child and path-commanded by node
		preceders = set([x for x in node.child.terminals_dominated
						 if node.path_commands(x)])
		followers = set([x for x in node.head.terminals_dominated
						 if node.path_commands(x)])
		return((preceders,followers))


