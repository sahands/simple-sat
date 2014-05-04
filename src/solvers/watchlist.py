from __future__ import division
from __future__ import print_function

from collections import deque
from sys import stderr


__author__ = 'Sahand Saba'
__email__ = 'sahands@gmail.com'


def dump_watchlist(instance, watchlist):
    print('Current watchlist:', file=stderr)
    for l, w in enumerate(watchlist):
        literal_string = instance.literal_to_string(l)
        clauses_string = ', '.join(instance.clause_to_string(c) for c in w)
        print('{}: {}'.format(literal_string, clauses_string), file=stderr)


def setup_watchlist(instance):
    watchlist = [deque() for __ in range(2 * len(instance.variables))]
    for clause in instance.clauses:
        # Make the clause watch its first literal
        watchlist[clause[0]].append(clause)
    return watchlist


def update_watchlist(instance,
                     watchlist,
                     false_literal,
                     assignment,
                     verbose):
    """
    Updates the watch list after literal 'false_literal' was just assigned
    False, by making any clause watching false_literal watch something else.
    Returns False it is impossible to do so, meaning a clause is contradicted
    by the current assignment.
    """
    while watchlist[false_literal]:
        clause = watchlist[false_literal][0]
        found_alternative = False
        for alternative in clause:
            v = alternative >> 1
            a = alternative & 1
            if assignment[v] is None or assignment[v] == a ^ 1:
                found_alternative = True
                del watchlist[false_literal][0]
                watchlist[alternative].append(clause)
                break

        if not found_alternative:
            if verbose:
                dump_watchlist(instance, watchlist)
                print('Current assignment: {}'.format(
                      instance.assignment_to_string(assignment)),
                      file=stderr)
                print('Clause {} contradicted.'.format(
                      instance.clause_to_string(clause)),
                      file=stderr)
            return False
    return True
