#! /usr/bin/python

from itertools import permutations

from bin.mtree import *
from bin.gen import *
from bin.con import *
from bin.tableau import *

basic = parseTreeFile('trees/basic.txt')
basicmv = parseTreeFile('trees/basic-mvnt.txt')
headmv = parseTreeFile('trees/basic-head.txt')
treelist = [basic, basicmv, headmv]

antisym = Antisymmetry()
hf = HeadFinality()
hfbp = HeadFinality(alpha='BP')
conlist = [antisym,hf,hfbp]


outputs = list(gen_strings(basic))

v_anti = {o: antisym(basic,o) for o in outputs}
v_hf = {o: hf(basic,o) for o in outputs}
v_hfa = {o: hfbp(basic,o) for o in outputs}


test = Typology(treelist,conlist)

for lang in test.languages.inverse:
	print(str(lang) + str(test.languages.inverse[lang]))
	print()

