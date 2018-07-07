#! /usr/bin/python

"""

Provides the Tableau class. A tableau takes an input, a iterable of
Constraints, and (optionally) a Gen fuction; it calculates all the violation
vectors and stores them in a bidirectional dictionary, then identifies the
winners based on reranking.

"""

from gen import Gen
from itertools import permutations
from operator import itemgetter



class bidict(dict):
    def __init__(self, *args, **kwargs):
        super(bidict, self).__init__(*args, **kwargs)
        self.inverse = {}
        for key, value in self.items():
            self.inverse.setdefault(value,[]).append(key) 

    def __setitem__(self, key, value):
        if key in self:
            self.inverse[self[key]].remove(key) 
        super(bidict, self).__setitem__(key, value)
        self.inverse.setdefault(value,[]).append(key)        

    def __delitem__(self, key):
        self.inverse.setdefault(self[key],[]).remove(key)
        if self[key] in self.inverse and not self.inverse[self[key]]: 
            del self.inverse[self[key]]
        super(bidict, self).__delitem__(key)


class Tableau:
	def __init__(self, inp, constraints, gen_func = None):
		self.input = inp
		self.constraints = tuple(constraints)
		if gen_func:
			self.gen = Gen(function=gen_func)
		else: self.gen = Gen()
		self.vectors = self._eval_constraints()
		self.contenders = self._find_contenders()
	
	def _eval_constraints(self):
		vectors = bidict()
		for candidate in self.gen(self.input):
			vectors[candidate] = tuple([con(self.input,candidate) 
									for con in self.constraints])
		return(vectors)

	def _find_contenders(self):
		# The general process:
		# for each possible constraint ranking:
		#	sort the bidict.inverse accordingly
		#	take the first item
		#	save the candidates in a set
		# Except we won't rerank the constraints; instead, we'll just generate
		# possible tuples of range(n).
		contenders = set()
		for ranking in permutations(range(len(self.constraints))):
			winning_vector = sorted(self.vectors.inverse.keys(),
									key=itemgetter(*ranking))[0]
			contenders.update(self.vectors.inverse[winning_vector])
		return(contenders)



