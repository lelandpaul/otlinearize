#! /usr/bin/python


""" 

Provides the MTree class, which instantiates multidominant trees made up of
the Node class.

"""


class Node(object):

	def __init__(self,
				name,
				mother = None,
				head = None,
				child = None):
		self.name = name
		self.mother = mother
		self.head = head
		self.child = child

	def isTerminal(self):
		return(not (head and child))

	def isRoot(self):
		return(not mother)

