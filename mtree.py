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
		if isinstance(mothers,Node): self.mothers = [mothers]
		else: self.mothers = mothers
		self.head = head
		self.child = child
		
		self.paths = []
		if self.mothers == []: self.paths = [(self,)]
		for mom in self.mothers:
			for path in mom.paths:
				self.paths.append(path + (self,))

	def getDaughters(self):
		return((self.head,self.child))

	def addMother(self,new_mom):
		if self.name[0] == new_mom.name[0] and new_mom.head:
			raise ValueError(str(new_mom) + #
					" already has head " + str(new_mom.head))
		elif new_mom.child:
			raise ValueError(str(new_mom) + #
					" already has child " + str(new_mom.child))
		self.mothers.append(new_mom)
		for path in new_mom.paths:
			self.paths.append(path + (self,))

	def isTerminal(self):
		return(not (self.head and self.child))

	def isRoot(self):
		return(not self.mothers)

	def getProjection(self):
		# Returns the mother that is also a projection
		for mom in self.mothers:
			if mom.head == self: return(mom)
		return(None)

	def getSisters(self):
		# Yields the sisters (if any)
		for mom in self.mothers:
			for n in mom.getDaughters():
				if n and n != self: yield n

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
		new_node = Node(name,mothers)
		for mom in new_node.mothers:
			if name[0] == mom.name[0]:
				if mom.head:
					raise ValueError(str(mom) + 
							" already has head " + str(mom.head))
				mom.head = new_node
			else: 
				if mom.child:
					raise ValueError(str(mom) + 
							" already has child " + str(mom.child))
				mom.child = new_node
		self.nodes.append(new_node)
		return(new_node)

	def getNode(self,name):
		# Returns the node with the given name
		return([n for n in self.nodes if n.name == name][0])

	def getNodeNames(self):
		# returns all node names
		return([n.name for n in self.nodes])

	def getTerminals(self):
		# Returns all terminal nodes
		return([n for n in self.nodes if n.isTerminal()])



# t = MTree("A")
# a = t.root
# b = t.addNode("B",a)
# c = t.addNode("C",b)
# c.addMother(a)
