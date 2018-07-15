# OTLinearize

Tools for calculating the linearization of syntactic structures using
Optimality Theory (Prince & Smolensky 1993/2004). This toolset was developed
as a proof of concept implementation for Optimal Linearization and the specific
constraints used in that framework, but includes some modules which may be
useful for testing other OT linearization schemes.

# Installation

Download the source manually or clone the repository:

```
git clone https://github.com/lelandpaul/otlinearize.git
```

# Basic usage

```
OT Linearization.

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
```

otlinearize.py has two main functions:

1. `tableau`: Create a tableau for a single tree:

```
$ python otlinearize.py tableau trees/basic.txt

basic      Antisymmetry    HeadFinality    HeadFinality-BP
-------  --------------  --------------  -----------------
acb                   1               1                  0
abc                   0               2                  1
cba                   3               0                  0
```

2. `typology`: Compute the full factorial typology for a given set of trees:

```
$ python otlinearize.py typology trees/basic.txt trees/basic-head.txt trees/basic-mvnt.txt

+-----------------------------------------------+---------+--------------+--------------+
| Ranking Conditions                            | basic   | basic-head   | basic-mvnt   |
+===============================================+=========+==============+==============+
| (Antisymmetry,)                               | abc     | bac          | cab          |
+-----------------------------------------------+---------+--------------+--------------+
| (HeadFinality, Antisymmetry)                  | cba     | cba          | cba          |
+-----------------------------------------------+---------+--------------+--------------+
| (HeadFinality-BP, Antisymmetry, HeadFinality) | acb     | bac          | cab          |
+-----------------------------------------------+---------+--------------+--------------+
```


## Tableaux

The `tableau` command takes a single tree specification file (in the format
specified below), evaluates it against the three basic Optimal Linearization
constraints, and outputs a tableau. All candidates are evaluated, but by
default only contenders are printed; use the `--all` flag to include
harmonically-bounded candidates.

## Typology

The `typology` command takes a list of tree files; you can either pass these in
as arguments, or use the `-f <treelist>` option, which takes a file with one
path per line.

The output has one column per input and one row per resulting language, listing
the winning candidate(s) in each cell. Languages are specified by ranking
conditions that have one of the following forms and interpretations:

1. (X,): Constraint X is undominated.
2. (X, Y): Constraint X always dominates constraint Y.
3. (X, Y, Z...): One specific ranking generates this language.

Forms (1) and (2) can be combined. 

## Other options

By default, the constraint set includes HeadFinality-BP, i.e. a version of
HeadFinality relativized to the node labelled BP. To specify a different
domain, use the option `--alpha=NODE`.

The option `--latex` will cause the output to be formatted as a LaTeX `tabular`
environment.

The option `-t` will print all of the trees in labelled-bracket form before the
table.


# Tree specification

The `MTree` class provides a specification for working with multidominant
syntax trees. This specification is limited in the following respects:

1. All trees must have a unique root.
2. All trees are at most binary.
3. Each terminal must have a unique label.
4. Internal nodes are labelled algorithmically such that:
	- X0 is a terminal node.
	- X is a branching word (created by head movement)
	- X1 (X2, ...) is the 1st (2nd, ...) projection of X.

Two shortcuts are provided for referencing nodes (useful for the `--alpha`
option):
- 'X' will map to X if it exists and X0 if not.
- 'XP' will map to the maximal projection of X.

The easiest way to build trees is to write a tree specification file, which
have the following format:

```
A, B, C # Comma-separated list of terminals
C0		# C0 projects
B0, C1	# Merge B0 with C1 and project B1
A0, B0	# Head-move B: [A A0 B0 ]
A, B1
A1, C1	# Phrase-move CP
```

Some things to note:
- `#` starts a line-end comment
- The first line must list all terminals
- A line with just a single node name indicates unary projection
- Comma-separated merge statements `X, Y` indicate that X merges with Y and
  projects.
- Merge statements can be made in any order, but it's advised to stick to
  bottom-up.

# Advanced usage

If you need to evaluate particularly large typologies or want a different
constraint set, you're probably better off writing your own evaluation script.
The `otlinearize` module provides several useful classes:

- `otlinearize.Typology(tree_list, constraint_list, gen = gen_strings)`

A typology is a list of tableau that all share a given `constraint_list` and
`gen` function. See `bin/tableau.py` for more details.

- `otlinearize.Tableau(tree, constraint_list, gen = gen_strings)`

A tableau takes a tree and a list of constraints (and a `gen` function),
evaluates those constraints, and picks winners. See `bin/tableau.py` for more
details.

- `otlinearize.parseTreeFile(file, name = None)`

Takes the path to a tree file, returns an `MTree`. By default, the tree is
given its filename, but you can override that here.

## New constraints

The three core linearization constraints are implemented in `bin/con.py`. A
class `LinConstraint` is provided as the basis for further such constraints;
you should subclass this to create any further constraints.

