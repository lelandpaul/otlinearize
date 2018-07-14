#! /usr/bin/python

"""
Provides functions for pretty-printing various objects used by Optimal
Linearization.

"""


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


