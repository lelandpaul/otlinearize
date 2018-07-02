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
		daughters = (head,child)

	def addMother(self,new_mom):
		self.mothers.append(new_mom)

	def isTerminal(self):
		return(not (head and child))

	def isRoot(self):
		return(not mother)

	def getProjection(self):
		# Returns the mother that is also a projection
		for mom in self.mothers:
			if mom.head = self: return(mom)
		return(None)

	def __repr__(self):
		return(self.name)


class MTree(object):

	def __init__(self,
				 root_name):
		self.root = Node(root_name)
		self.nodes = [self.root]

	def addNode(self,name,mothers):
		# Adds a new child node with given name, mothers
		if name in self.getNodeNames():
			raise ValueError("Name not unique.")
		self.nodes.append(Node(name,mothers))

	def getNode(self,name):
		# Returns the node with the given name
		return([n for n in self.nodes if n.name == name][0])

	def getNodeNames(self):
		# returns all node names
		return([n.name for n in self.nodes])

	def getSisters(self,node):
		# Yields the sister nodes (if any) of a given node
		for mom in node.mothers:
			for n in mom.daughters:
				if n != node: yield n

	def getTerminals(self):
		# Returns all terminal nodes
		return([n for n in self.nodes if n.isTerminal()])

	def getPaths(self,node):
		# Yields all paths from a given terminal node
		# Basically: Do DFS upward from the node, yield once you get to the root
		pass



