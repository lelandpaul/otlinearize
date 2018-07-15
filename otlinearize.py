#! /usr/bin/python


"""OT Linearization.

Usage:
    otlinearize.py [options]
    otlinearize.py tableau [options] <tree>
    otlinearize.py typology [options] <trees>...
    otlinearize.py typology [options] -f <treelist>

Options:
    -h, --help     Show this screen.
    --version      Show version.
    -t             Print trees in labelled-bracket form before output.
    -a, --all      For tableau: output all candidates (not just contenders).
    --latex        Output in LaTeX format (as opposed to ASCII).
    --alpha=NODE   Use the default constraints, but specify HF-alpha.
"""


from docopt import docopt
from itertools import permutations
import tabulate

from bin.mtree import *
from bin.gen import *
from bin.con import *
from bin.tableau import *

if __name__ == '__main__':

	args = docopt(__doc__,version='OTLinearize 1.0')

	# Build our Con:
	conlist = [ Antisymmetry(),
				HeadFinality(),
				HeadFinality(alpha = 'BP' if not args['--alpha']
										  else args['--alpha']),
				]

	if args['tableau']:
		# We're making a single tableau; get the tree.
		tree = parseTreeFile(args['<tree>'])

		# now build the tableau:
		output = Tableau(tree, conlist)

		# If -t is set:
		if args['-t']:
			print(tabulate.tabulate([(str(tree),tree.bracket_string())],tablefmt='plain'))
			print()

		# Output appropriately:
		if args['--latex']:
			print(output.print_tabular(include_bounded=args['--all']))
		else:
			print(output.print_ascii(include_bounded=args['--all']))


	elif args['typology']:
		# We're making a typology. Either we've been given a list of tree files
		# directly, or we need to parse one.

		if args['<trees>']:
			trees = args['<trees>']
		elif args['<treelist>']:
			with open(args['<treelist>'],'r') as treef:
				trees = treef.read()
				trees = trees.splitlines()
		treelist = [parseTreeFile(t) for t in trees]

		# Make our typology:
		output = Typology(treelist, conlist)

		# If -t is set:
		if args['-t']:
			print(tabulate.tabulate([(str(t),t.bracket_string()) for t in treelist],
				tablefmt='plain'))
			print()

		# Output appropriately:
		if args['--latex']:
			print(output.print_tabular())
		else:
			print(output.print_ascii())

	
	else:
		# No command, just freak out
		print(__doc__)
		quit()

