from __future__ import division
from __future__ import print_function

from watchlist import setup_watchlist
from watchlist import update_watchlist


__author__ = 'Sahand Saba'
__email__ = 'sahands@gmail.com'


def _solve(instance, watchlist, assignment, d, verbose):
    if d == instance.n:
        return True
    for a in [0, 1]:
        assignment[d] = a
        if update_watchlist(instance,
                            watchlist,
                            d << 1 | a ^ 1,
                            assignment,
                            verbose):
            if _solve(instance, watchlist, assignment, d + 1, verbose):
                return assignment

    assignment[d] = None
    return None


def solve(instance, verbose=False):
    n = len(instance.variables)
    watchlist = setup_watchlist(instance)
    if not watchlist:
        return None
    assignment = [None] * n
    return _solve(instance, watchlist, assignment, 0, verbose)
