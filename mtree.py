#! /usr/bin/python


""" 

Provides the MTree class, which instantiates multidominant trees made up of
the Node class.

An MTree is essentially a directed acyclic graph (DAG) with some extra
restrictions:
	- Nodes have at most 2 daughters
	- The 2 daughters of a Node are distinct: One is the head, one is the child
	- The head of a node shares a label with it
	- There is one unique Node with 0 mothers, called the root

"""


class TreeError(Exception):
	pass


class Node(object):

	def __init__(self,head,child):
		self.label = (head.label[0],head.label[1]+1) # project
		self.paths = [(self,)] # paths to root
		self.mothers = []

		self.head = head # the head Node
		self.head.add_mother(self) # add the upward edge

		self.child = child # the child Node
		if child: # this might be None
			self.child.add_mother(self) # add the upward edge

	def __repr__(self):
		return(self.label[0] + str(self.label[1]))

	@property
	def daughters(self):
		return((self.head,self.child))

	def add_mother(self,node):
		# add an additional mother
		self.mothers.append(node)
		self.update_paths() # update paths to match

	def update_paths(self):
		new_paths = []
		for mom in self.mothers:
			for path in mom.paths:
				new_paths.append(path + (self,))
		self.paths = new_paths
		# Now, propagate down:
		for daughter in self.daughters:
			if daughter: # this might be None
				daughter.update_paths()

class TerminalNode(Node):

	def __init__(self,name):
		self.label = (str(name),0)
		self.head = None
		self.child = None
		self.paths = [(self,)]
		self.mothers = []

	def update_paths(self):
		self.paths = []
		for mom in self.mothers:
			for path in mom.paths:
				self.paths.append(path + (self,))
