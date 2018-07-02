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
