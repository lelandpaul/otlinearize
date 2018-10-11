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

	def __init__(self,head,child,tree=None):
		if child and head.word and child.word:
			# special case for head-movement
			self.label = (head.label[0],head.label[1])
		else:
			self.label = (head.label[0],head.label[1]+1) # project

		self.paths = [(self,)] # paths to root
		self.projections = [self] # things projected
		self.mothers = []

		self.head = head # the head Node
		self.head.add_mother(self) # add the upward edge
		self.head.add_projection(self) # add the projection

		self.child = child # the child Node
		if child: # this might be None
			self.child.add_mother(self) # add the upward edge

		self.terminal = False
		self.tree = tree

	def __repr__(self):
		# if self.label[1] == 0:
		# 	return(self.label[0]) # special case for complex heads
		return(self.label[0] + str(self.label[1]))

	@property
	def daughters(self):
		return((self.head,self.child))

	def add_mother(self,node):
		# add an additional mother
		self.mothers.append(node)
		self.update_paths() # update paths to match

	def add_projection(self,node):
		self.projections.append(node)
		if not self.terminal:
			self.head.add_projection(node) # propagate down

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

	@property
	def branching(self):
		return(self.head and self.child)

	@property
	def word(self):
		return(self.label[1] == 0)

	def dominates(self,target):
		# target is a node. true if self dominates target.
		return(bool([p for p in target.paths if self in p]))

	@property
	def terminals_dominated(self):
		# returns all terminals dominated by this node
		return(self.tree.terminals_dominated(self))

	@property
	def dominators(self):
		# returns all nodes that dominate this one
		# defined to be non-reflexive, for c-command reasons
		return(set(self.tree.dominators_of(self)) - {self})

	def ccommand(self,target):
		# returns true if this node ccommands the target
		# ccommand is defined in terms of dominator subsets
		return(self.dominators <= target.dominators)

	def path_command(self,target):
		# true if all paths from the target passes through a projection of this
		# node.
		for path in target.paths:
			# we want to only track the thing and its immediate projection
			if not set(path) & set(self.projections[:2]):
				return(False)
		return(True)

class TerminalNode(Node):

	def __init__(self,name,tree = None):
		self.label = (str(name),0)
		self.head = None
		self.child = None
		self.paths = [(self,)]
		self.projections = [self]
		self.mothers = []
		self.terminal = True
		self.tree = tree

	def __repr__(self):
		# special case: keep the 0 rank, but don't print it
		# this will make terminal nodes accessible via "X" rather than "X0"
		return(self.label[0])

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

	def __init__(self,terminals,merges,name = None):
		self.terminals = [TerminalNode(n, tree = self) for n in terminals]
		self.nodes = {str(n): n for n in self.terminals}
		self.root = None
		self.name = name

		# build it

		roots = list(self.terminals)
		while merges:
			cur_merge = merges.pop(0) # get the first one

			# We need to check if we've created both nodes.
			# And we want to do this in a way that takes advantage of the
			# alternate naming schemes defined in __getitem__
			# so "if ___ not in ___" won't cut it.
			# This is the alternative:
			try:
				self[cur_merge[0]] # have we created node 1?
				if cur_merge[1]: # might be null
					self[cur_merge[1]] # have we created node 2?
			except KeyError: # one of them didn't exist
				if cur_merge[1]: # this might be null
					# if it's null, we actually can continue, even with the
					# exception.
					merges.append(cur_merge)
					continue # skip this instruction until we've built more
			
			# find the head
			head = self[cur_merge[0]]
			try: roots.remove(head)
			except ValueError: pass # wasn't there

			# find the child, if applicable
			if cur_merge[1]: # this might be None
				child = self[cur_merge[1]]
				try: roots.remove(child)
				except ValueError: pass
			else: child = None

			# make a new node
			new_node = Node(head,child,tree = self)
			# This is a root now:
			roots.append(new_node)
			# Make sure we keep track of this node:
			self.nodes[str(new_node)] = new_node

		# Ok, we've built a tree. Check if it has a unique root:
		if len(roots) > 1:
			raise TreeError("No unique root:" + str(roots))
		self.root = roots[0] # ok, we succeeded

	def __getitem__(self,item):
		# This needs to do slightly more than just get the node:
		# - X0 gets interpreted as X in the absence of X0
		# - XP gets interpreted as "maximal projection of X"
		try:
			return(self.nodes[item])
		except KeyError:
			if item[-1] == '0':
				return(self.nodes[item[:-1]])
			if item[-1] == 'P':
				head = self.nodes[item[:-1]]
				return(head.projections[-1]) # the maximal one is added last
			raise(KeyError)

	def __iter__(self):
		yield from self.nodes.values()

	@property
	def branching_nodes(self):
		yield from [n for n in self.nodes.values() if n.branching]

	@property
	def nonterminal_nodes(self):
		yield from [n for n in self.nodes.values() if n.terminal]

	@property
	def words(self):
		yield from [n for n in self.nodes.values() if n.word]

	def terminals_dominated(self,node):
		# returns the terminal nodes dominated by node
		return([n for n in self.terminals if node.dominates(n)])

	def dominators_of(self,node):
		# returns the nodes that dominate a given node
		return([n for n in self.nodes.values() if n.dominates(node)])

	### printing

	def bracket_string(self, qtree = False):
		# prints the tree in labeled-bracket form
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

		return(_recurse_on_node(self.root))

	def __repr__(self):
		if self.name: return(self.name)
		return(self.bracket_string())


def parseTreeFile(fname,name = None):
	"""
	Wrapper for parseTreeString; gets it from a file.
	Name defaults to the filename.
	"""

	with open(fname,"r") as f:
		treestring = f.read()

	if name is None:
		name = fname.split('.')[0].split('/')[-1] # remove extension and path

	return(parseTreeString(treestring,name=name))


def parseTreeString(string,name=None):
	"""
	Takes a string in the following format:
	A, B, C		# terminals in  one line, comma separated,
	A0			# Unary merge
	B0, A1		# one merge per line
	B1, C0		# line-end comments and whitespace are ignored
	"""

	# First, split the string
	string = string.splitlines()
	# ditch comments:
	treestring = [x.split('#')[0] for x in string]

	terminals = treestring.pop(0)
	terminals = ''.join(terminals.split()).split(',') # munge
	terminals = [t for t in terminals if t] # remove nulls

	merge_list = []
	for line in treestring:
		line = ''.join(line.split()).split(',') #munge
		head = line[0]
		try: child = line[1]
		except IndexError:
			child = None
		merge_list.append((head,child))
	
	return(MTree(terminals,merge_list,name=name))
