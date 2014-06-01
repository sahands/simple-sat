from __future__ import print_function


def even_ones(s):
    # Two states:
    # - 0 (even number of ones seen so far)
    # - 1 (odd number of ones seen so far)
    rules = {(0, '0'): 0,
             (0, '1'): 1,
             (1, '0'): 1,
             (1, '1'): 0}
    # There are 0 (which is an even number) ones in the empty
    # string so we start with state = 0.
    state = 0
    for c in s:
        state = rules[state, c]
    return state == 0


# Example usage:
s = "001100110"
print('Output for {} = {}'.format(s, even_ones(s)))
