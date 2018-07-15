#! /usr/bin/python

"""

Provides the Tableau class. A tableau takes an input, a iterable of
Constraints, and (optionally) a Gen with a custom function; it calculates all
the violation vectors and stores them in a bidirectional dictionary, then
identifies the winners based on reranking.


Also provides the Typology class. A typology is a set of tableaux that all
share the same constraint set and gen. It maintains a master dictionary of
{ranking: outputs}.

"""

from bin.gen import Gen
from math import factorial
from itertools import permutations
from operator import itemgetter
import tabulate



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
	def __init__(self, inp, constraints, gen = Gen()):
		self.input = inp
		self.constraints = tuple(constraints)
		self.gen = gen
		self.vectors = self._eval_constraints()
		self._contender_dict = self._find_contenders()
	
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
		contenders = bidict()
		for ranking in permutations(range(len(self.constraints))):
			winning_vector = sorted(self.vectors.inverse.keys(),
									key=itemgetter(*ranking))[0]
			contenders[tuple(ranking)] = tuple(self.vectors.inverse[winning_vector])
		return(contenders)

	@property
	def contenders(self):
		winners = set()
		for item in self._contender_dict.inverse.keys():
			winners.update(item)
		return(winners)

	def get_winners(self,ranking):
		# expects the constraints ranked in some order
		order = tuple([self.constraints.index(con) for con in ranking])
		return(tuple(self._contender_dict[order]))

	### printing


	def _make_table(self, include_bounded = False):
		# Formats the tableau for tabulate
		# if bounded is set, it includes all candidates; otherwise only contenders
		constraints = list(self.constraints)
		inp = self.input

		winners = {w: self.vectors[w] for w in self.contenders}
		if include_bounded:
			bounded = {c: self.vectors[c] 
					   for c in self.vectors 
					   if c not in winners}
		else: bounded = []

		header = [str(inp)] + [str(x) for x in constraints]

		rows = []
		for winner in winners:
			rows.append([winner] + list(winners[winner]))
		for loser in bounded:
			rows.append([loser] + list(bounded[loser]))

		return((rows,header))

	def print_ascii(self, include_bounded=False):
		return(tabulate.tabulate(*self._make_table(include_bounded)))


	# def print_ascii(self,include_bounded = False):
	# 	# Formats the tableau in a nice way
	# 	# if bounded is set, it includes all candidates; otherwise only contenders
	# 	constraints = list(self.constraints)
	# 	inp = self.input
	# 	col_lengths = [len(str(x)) + 2 for x in [inp] + constraints]
		
	# 	output = []
	# 	output.append('-' + '-'.join(['-'*length for length in col_lengths]) + '-')
	# 	output.append('|' + '|'.join([f' {x} ' for x in [inp] + constraints]) + '|')
	# 	output.append('=' + '='.join(['='*length for length in col_lengths]) + '=')

	# 	winners = {w: self.vectors[w] for w in self.contenders}
	# 	if include_bounded:
	# 		bounded = {c: self.vectors[c] 
	# 				   for c in self.vectors 
	# 				   if c not in winners}
	# 	else: bounded = []

	# 	for winner in winners:
	# 		items = (winner,) + winners[winner]
	# 		output.append('|' + '|'.join([f"{i:^{j}}" 
	# 								for i, j in zip(items,col_lengths)]) + '|')
		
	# 	if include_bounded:
	# 		output.append('-' + \
	# 				'-'.join(['-'*length for length in col_lengths]) + '-')
	# 	for loser in bounded:
	# 		items = (loser,) + bounded[loser]
	# 		output.append('|' + '|'.join([f"{i:^{j}}" 
	# 								for i, j in zip(items,col_lengths)]) + '|')
		

	# 	output.append('-' + '-'.join(['-'*length for length in col_lengths]) + '-')

	# 	return('\n'.join(output))


	def print_tabular(self, include_bounded= False):
		# Formats a tableau as a latex tabular environment
		# if bounded is set, includes all candidates; otherwise, only contenders
		# if the input has a name, it assumes that's a reference

		# LPK: writing this myself, since I want slightly different formatting
		# than tabulate's latex style.

		inp = self.input
		constraints =  list(self.constraints)

		con_names = ' & '.join([f'\\textsc{{{c}}}' for c in constraints])

		winners = {w: self.vectors[w] for w in self.contenders}
		if include_bounded:
			bounded = {c: self.vectors[c] 
					   for c in self.vectors 
					   if c not in winners}
		else: bounded = []


		def cand_rows(candidates):
			output = []
			for c in candidates:
				row = f"{c} & " + \
						" & ".join([f'{v}' for v in candidates[c]]) +\
						"\\\\"
				output.append(row)
			return('\n'.join(output))

		output = r"\begin{tabular}" f"{{|r||{'c|'*len(constraints)}}}\n" \
				 f"\\ref{{{inp}}} & {con_names} \\\\\n" \
				 f"\\hline\n\\hline\n" \
				 f"{cand_rows(winners)}\n"

		if include_bounded:
			output += "\\hline\n" \
					  f"{cand_rows(bounded)}\n"
		
		output += "\\hline\n"

		return(output)

	def __repr__(self):
		return(self.print_ascii())



class Typology:
	def __init__(self, inputs, constraints, gen = Gen()):
		self.inputs = tuple(inputs)
		self.constraints = tuple(constraints)
		self.gen = gen
		self.tableaux = [Tableau(inp,constraints,gen = self.gen)
						for inp in self.inputs]

		self.languages = bidict()
		for ranking in permutations(self.constraints):
			self.languages[ranking] = tuple([tab.get_winners(ranking) for
										tab in self.tableaux])

	@property
	def size(self):
		return(len(self.languages.inverse))

	def __getitem__(self,inp):
		for tableau in self.tableaux:
			if tableau.input == inp:
				return(tableau)
		raise IndexError('No such input.')

	### printing

	def summarize_rankings(self,rankingset):
		# Takes a list of rankings and expresses it in a condensed format:
		# - if n=1: Return a list containing that one
		# - if n=c!: return an empty list
		# otherwise, return a list:
		# - if X is always undominated, the list includes (X,)
		# - if X always dominates Y (but X is dominated at least once), the set
		# includes (X,Y)

		# Base-cases first:

		if len(rankingset) == 1: return(list(rankingset))
		if len(rankingset) == factorial(len(rankingset[0])):
			return([])

		# Is anything always undominated?
		dominators = {ranking[0] for ranking in rankingset}
		if len(dominators) == 1:
			undominated = [(list(dominators)[0],)]
		else: undominated = []

		# Convert each ranking into a set of binary ranking statements
		# if we've found an undominated thing, we can just ignore it
		binarize = lambda ranking: set([ (ranking[i], ranking[j])
									  for i in range(len(ranking)-1)
									  for j in range(i+1,len(ranking)) ])
		if undominated: _u = lambda x: x[1:]
		else: _u = lambda x: x
		bin_rankings = [binarize(_u(ranking)) for ranking in rankingset]
		bin_rankings = set.intersection(*bin_rankings) # reduce

		return(undominated + list(bin_rankings))


	def _make_table(self):
		# assembles the tabular version

		header = ['Ranking Conditions'] + [str(t.input) for t in self.tableaux]

		rows = []
		for lang in self.languages.inverse:
			ranking_con = self.summarize_rankings(self.languages.inverse[lang])
			ranking_con = '\n'.join([f'{x}' for x in ranking_con])
			outputs = [', '.join(l) for l in lang]
			rows.append([ranking_con] + outputs)

		return((rows,header))

	def print_ascii(self):
		return(tabulate.tabulate(*self._make_table(),tablefmt='grid'))

	def print_tabular(self):
		return(tabulate.tabulate(*self._make_table(),tablefmt='latex'))

	def __str__(self):
		return(self.print_ascii())







