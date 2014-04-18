from __future__ import division
from __future__ import print_function

__author__ = 'Sahand Saba'


class SATInstance(object):
    def _parse_and_add_clause(self, line):
        """
        Some notes on encoding:
        - Variables are encoded as numbers 0 to n - 1.
        - Literal v is encoded as 2 * v and ~v as 2 * v + 1. So the foremost
          bit of a literal encodes whether it is negated or not. This can be
          tested simply with checking if l & 1 is 0 or 1.
        - Similarly, to negate a literal, we just have to toggle the foremost
          bit.  This can done easily by XORing with 1: the negation l is l ^ 1.
        - To get a literal's variable, we just need to shift to the right. This
          can be done with either l >> 1.

        Example: Let's say variable b is encoded with number 3. Then literal b
        is encoded as 2 * 3 = 6 and ~b as  2 * 3 + 1 = 7.
        """
        clause = []
        for literal in line.split():
            negated = 1 if literal.startswith('~') else 0
            variable = literal[negated:]
            if variable not in self.variable_table:
                self.variable_table[variable] = len(self.variables)
                self.variables.append(variable)
            encoded_literal = self.variable_table[variable] << 1 | negated
            clause.append(encoded_literal)
        self.clauses.append(tuple(set(clause)))

    @classmethod
    def from_file(cls, file):
        instance = cls()
        instance.variables = []
        instance.variable_table = dict()
        instance.clauses = []
        for line in file:
            line = line.strip()
            if len(line) > 0 and not line.startswith('#'):
                instance._parse_and_add_clause(line)
        instance.n = len(instance.variables)
        return instance

    def literal_to_string(self, literal):
        s = '~' if literal & 1 else ''
        return s + self.variables[literal >> 1]

    def clause_to_string(self, clause):
        return ' '.join(self.literal_to_string(l) for l in clause)

    def assignment_to_string(self, assignment, brief=False):
        if brief:
            return ' '.join(v for i, v in enumerate(self.variables)
                            if assignment[i])
        else:
            return ' '.join(v if assignment[i] else '~' + v
                            for i, v in enumerate(self.variables)
                            if assignment[i] is not None)
