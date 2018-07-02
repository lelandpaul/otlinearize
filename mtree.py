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



class MTree(object):
	"""
	An MTree object.

	MTree(terminals,merges)

	terminals - list of strings labelling terminal nodes
	merges - list of tuples (head, child) indicating merges
	"""

	def __init__(self,terminals,merges):
		self.terminals = (TerminalNode(n) for n in terminals)
		self.nodes = {str(n): n for n in self.terminals}
		self.root = None

		# build it

		roots = list(self.terminals)
		while merges:
			cur_merge = merges.pop(0) # get the first one
			if cur_merge[0] not in self.nodes or cur_merge[1] not in self.nodes:
				   # We haven't created the necessary nodes yet,
				   # so skip it and come back
				merges.append(cur_merge)
				continue

			# Create a new node
			head = self.nodes[cur_merge[0]]
			child = self.nodes[cur_merge[1]]
			# remove these from roots:
			try: roots.remove(head)
			except ValueError: pass # wasn't there
			try: roots.remove(child)
			except ValueError: pass

			new_node = Node(head,child)
			# This is a root now:
			roots.append(new_node)
			# Make sure we keep track of this node:
			self.nodes[str(new_node)] = new_node

		# Ok, we've built a tree. Check if it has a unique root:
		if len(roots) > 1:
			raise TreeError("No unique root.")
		self.root = roots[0] # ok, we succeeded


