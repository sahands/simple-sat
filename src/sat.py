#!/usr/bin/env python
"""
Solves SAT instance by reading from stdin using an iterative or recursive
watchlist-based backtracking algorithm. Iterative algorithm is used by default,
unless the --recursive flag is given. Empty lines and lines starting with a #
will be ignored.
"""
from __future__ import division
from __future__ import print_function

from argparse import ArgumentParser
from argparse import FileType
from sys import stdin
from sys import stdout
from sys import stderr

from satinstance import SATInstance
from solvers.watchlist import setup_watchlist
from solvers import recursive_sat
from solvers import iterative_sat

__author__ = 'Sahand Saba'


def generate_assignmnets(instance, solver, verbose=False):
    """
    Returns a generator that generates all the satisfying assignments for a
    given SAT instance, using algorithm given by alg.
    """
    n = len(instance.variables)
    watchlist = setup_watchlist(instance)
    if not watchlist:
        return ()
    assignment = [None] * n
    return solver.solve(instance, watchlist, assignment, 0, verbose)


def run_solver(input_file, output_file, solver, brief, verbose, output_all,
               starting_with):
    """
    Run the given solver for the given file-like input object and write the
    output to the given output file-like object.
    """
    instance = SATInstance.from_file(input_file)
    assignments = generate_assignmnets(instance, solver, verbose)
    count = 0
    for assignment in assignments:
        count += 1
        if verbose:
            print('Found satisfying assignment #{}:'.format(count),
                  file=stderr)
        assignment_str = instance.assignment_to_string(
                assignment,
                brief=brief,
                starting_with=starting_with
        )
        output_file.write(assignment_str + '\n')
        if not output_all:
            break

    if verbose and count == 0:
        print('No satisfying assignment exists.', file=stderr)


def main():
    args = parse_args()
    with args.input:
        with args.output:
            run_solver(args.input, args.output, args.solver, args.brief,
                       args.verbose, args.all, args.starting_with)


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
    parser.add_argument('-b',
                        '--brief',
                        help=('brief output:'
                              ' only outputs variables assigned true.'),
                        action='store_true')
    parser.add_argument('--starting_with',
                        help=('only output variables with names'
                              ' starting with the given string.'),
                        default='')
    parser.add_argument('--iterative',
                        help='use the iterative algorithm.',
                        action='store_const',
                        dest='solver',
                        default=recursive_sat,
                        const=iterative_sat)
    parser.add_argument('-i',
                        '--input',
                        help='read from given file instead of stdin.',
                        type=FileType('r'),
                        default=stdin)
    parser.add_argument('-o',
                        '--output',
                        help='write to given file instead of default stdout.',
                        type=FileType('w'),
                        default=stdout)
    return parser.parse_args()


if __name__ == '__main__':
    main()
