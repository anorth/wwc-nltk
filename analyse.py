#!/usr/bin/env python
import argparse
import sys

import nltk
from nltk import FeatureChartParser
from nltk.grammar import FeatureGrammar, FeatStructNonterminal


def load_grammars(grammar_paths, start_symbol=None):
  """Loads grammars from a list of files and combines them into a single feature grammar"""
  if start_symbol is None:
    start_symbol = FeatStructNonterminal('Sentence')
  productions = []
  for path in grammar_paths:
    g = nltk.data.load(path, format='fcfg')
    productions.extend(g.productions())
  grammar = FeatureGrammar(start_symbol, productions)
  return grammar


def main(argv):
  """
  Loads grammar files from command-line args then parses lines from standard input.
  """
  parser = argparse.ArgumentParser()
  parser.add_argument(dest='grammars', nargs='+',
    help='Grammar file path(s)')
  parser.add_argument('--draw', dest='draw', action='store_true',
    help='Draw trees')
  parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
    help='Be verbose')
  args = parser.parse_args(argv)

  grammar = load_grammars(args.grammars)
  parser = FeatureChartParser(grammar, trace=args.verbose, trace_chart_width=80)

  for line in sys.stdin:
    if line[0] == '#': continue
    tokens = line.lower().strip().split()
    if len(tokens) == 0: continue

    trees = list(parser.parse(tokens))
    print('*** {} ***'.format(tokens))
    if trees:
      for tree in trees:
        print(tree.pformat(margin=80))
        if args.draw:
          tree.draw()
        # print(TreePrettyPrinter(tree).text())
    else:
      print('Could not parse {}'.format(tokens))
    print('\n')


if __name__ == '__main__':
  main(sys.argv[1:])
