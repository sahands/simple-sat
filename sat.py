"""
Solve SAT instance by reading from stdin using an iterative or recursive
watchlist-based backtracking algorithm. Iterative algorithm is used by default,
unless the -r flag is given.
"""
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from sys import stdin
from sys import stderr
from satinstance import SATInstance
import recursive_sat
import iterative_sat

__author__ = 'Sahand Saba'
__email__ = 'sahands@gmail.com'


if __name__ == '__main__':
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-v',
                        '--verbose',
                        help='verbose output.',
                        action='store_true')
    parser.add_argument('-r',
                        '--recursive',
                        help='use the recursive backtracking algorithm.',
                        action='store_true')
    parser.add_argument('-i',
                        '--input',
                        help='read from given file instead of stdin.',
                        action='store')
    args = parser.parse_args()
    instance = None
    if args.input:
        with open(args.input, 'r') as file:
            instance = SATInstance.from_file(file)
    else:
        instance = SATInstance.from_file(stdin)
    assignment = None
    if args.recursive:
        assignment = recursive_sat.solve(instance, args.verbose)
    else:
        assignment = iterative_sat.solve(instance, args.verbose)
    if assignment:
        if args.verbose:
            print('Found satisfying assignment.', file=stderr)
        print(instance.assignment_to_string(assignment))
    else:
        if args.verbose:
            print('No satisfying assignment exists.', file=stderr)
