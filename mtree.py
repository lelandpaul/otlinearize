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


class MTree(object):

	def __init__(self,
				 root_name):
		self.root = Node(root_name)
		self.nodes = [self.root]

	def addNode(self,name,mothers):
		# Adds a new child node with given name, mothers
		self.nodes.append(Node(name,mothers))

	def getNode(self,name):
		# Returns the node with the given name
		return([n for n in self.nodes if n.name = name][0])
		

	def getSisters(self,node):
		# Returns the sister nodes (if any) of a given node
		pass

	def getTerminals(self):
		# Returns all terminal nodes
		pass

	def getPaths(self,node):
		# Returns all paths from a given terminal node
		pass

