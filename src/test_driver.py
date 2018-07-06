#!/usr/bin/env python
import os
import unittest

from sat import run_solver
from solvers import recursive_sat
from solvers import iterative_sat
from io import StringIO


class TestAllInputs(unittest.TestCase):
    def run_test_case(self, input_file_path, solver):
        output_file_path = input_file_path.replace('.in', '.out')
        with open(input_file_path, 'r') as input_fp:
            with open(output_file_path, 'r') as output_fp:
                expected_output = output_fp.read()
                actual_output = StringIO()
                run_solver(input_fp, actual_output, solver, False, False,
                           False, '')
                self.assertEqual(expected_output, actual_output.getvalue())
                actual_output.close()


    def run_tests_with_solver(self, solver):
        for dirpath, _, filenames in os.walk('./tests'):
            for name in filenames:
                if name.endswith('.in'):
                    input_file_path = os.path.join(dirpath, name)
                    self.run_test_case(input_file_path, solver)

    def test_all_inputs_recursive(self):
        self.run_tests_with_solver(recursive_sat)

    def test_all_inputs_iteraive(self):
        self.run_tests_with_solver(iterative_sat)


if __name__ == '__main__':
    unittest.main()
