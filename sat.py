"""
Solve SAT instance by reading from stdin using an iterative or recursive
watchlist-based backtracking algorithm. Iterative algorithm is used by default,
unless the -r flag is given. Input lines starting with a # will be ignored.
"""
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from argparse import FileType
from sys import stdin
from sys import stderr

from satinstance import SATInstance
import recursive_sat
import iterative_sat

__author__ = 'Sahand Saba'


def main():
    args = parse_args()
    instance = None
    with args.input as file:
        instance = SATInstance.from_file(file)

    assignments = args.algorithm.solve(instance, args.verbose)
    count = 0
    for assignment in assignments:
        if args.verbose:
            print('Found satisfying assignment #{}:'.format(count),
                  file=stderr)
        print(instance.assignment_to_string(assignment))
        count += 1
        if not args.all:
            break

    if args.verbose and count == 0:
        print('No satisfying assignment exists.', file=stderr)


def parse_args():
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('-v',
                        '--verbose',
                        help='verbose output.',
                        action='store_true')
    parser.add_argument('-a',
                        '--all',
                        help='output all possible solutions.',
                        action='store_true')
    parser.add_argument('-r',
                        '--recursive',
                        help='use the recursive backtracking algorithm.',
                        action='store_const',
                        dest='algorithm',
                        default=iterative_sat,
                        const=recursive_sat)
    parser.add_argument('-i',
                        '--input',
                        help='read from given file instead of stdin.',
                        type=FileType('r'),
                        default=stdin)
    return parser.parse_args()


if __name__ == '__main__':
    main()
