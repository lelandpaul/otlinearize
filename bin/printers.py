#! /usr/bin/python

"""
Provides functions for pretty-printing various objects used by Optimal
Linearization.

"""

from math import factorial

from bin.mtree import *




### Printing Trees

def bracket_form(tree, qtree = False):
	# prints an mtree in labeled-bracket form
	# multidominance is handled by reusing a label (since labels are unique)
	# if qtree is set, it will print it in a form suitable for qtree.sty to
	# typeset
	# always prints in head-final ordering, because it's easier

	def _q(n):
		if qtree:
			return(f"[.{{{n}}}")
		return(f"[{n}")

	def _recurse_on_node(node):
		if node is None:
			return("")
		if node.terminal:
			# base case
			return(str(node))
		left = node.child
		right = node.head
		left = _recurse_on_node(left)
		right = _recurse_on_node(right)

		if left:
			return(f"{_q(node)} {left} {right} ]")
		return(f"{_q(node)} {right} ]")

	return(_recurse_on_node(tree.root))


def summarize_rankings(rankingset):
	# Takes a list of rankings and expresses it in a condensed format:
	# - if n=1: Return a list containing that one
	# - if n=c!: return an empty list
	# otherwise, return a list:
	# - if X is always undominated, the list includes (X,)
	# - if X always dominates Y (but X is dominated at least once), the set
	# includes (X,Y)

	# Base-cases first:

	if len(rankingset) == 1: return(list(rankingset))
	if len(rankingset) == factorial(len(rankingset[0])):
		return([])

	# Is anything always undominated?
	dominators = {ranking[0] for ranking in rankingset}
	if len(dominators) == 1:
		undominated = [(list(dominators)[0],)]
	else: undominated = []

	# Convert each ranking into a set of binary ranking statements
	# if we've found an undominated thing, we can just ignore it
	binarize = lambda ranking: set([ (ranking[i], ranking[j])
								  for i in range(len(ranking)-1)
								  for j in range(i+1,len(ranking)) ])
	if undominated: _u = lambda x: x[1:]
	else: _u = lambda x: x
	bin_rankings = [binarize(_u(ranking)) for ranking in rankingset]
	bin_rankings = set.intersection(*bin_rankings) # reduce

	return(undominated + list(bin_rankings))

