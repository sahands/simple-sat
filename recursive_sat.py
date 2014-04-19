from __future__ import division
from __future__ import print_function

from sys import stderr

from watchlist import setup_watchlist
from watchlist import update_watchlist


__author__ = 'Sahand Saba'
__email__ = 'sahands@gmail.com'


def _solve(instance, watchlist, assignment, d, verbose):
    if d == len(instance.variables):
        yield assignment
        return

    for a in [0, 1]:
        if verbose:
            print('Trying {} = {}'.format(instance.variables[d], a),
                  file=stderr)
        assignment[d] = a
        if update_watchlist(instance,
                            watchlist,
                            (d << 1) | a,
                            assignment,
                            verbose):
            for a in _solve(instance, watchlist, assignment, d + 1, verbose):
                yield a

    assignment[d] = None


def solve(instance, verbose=False):
    n = len(instance.variables)
    watchlist = setup_watchlist(instance)
    if not watchlist:
        return []
    assignment = [None] * n
    return _solve(instance, watchlist, assignment, 0, verbose)
