#! /usr/bin/python


""" 

Provides the MTree class, which instantiates multidominant trees made up of
the Node class.

"""


class Node(object):

	def __init__(self,
				name,
				mothers = [],
				head = None,
				child = None):
		self.name = name
		self.mothers = mothers
		self.head = head
		self.child = child

	def addMother(self,new_mom):
		self.mothers.append(new_mom)

	def isTerminal(self):
		return(not (head and child))

	def isRoot(self):
		return(not mother)

