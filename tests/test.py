
import sys
sys.path.append('../solve')
from solve import solve

import os
import glob
import nose

def parse_state(file):
    return tuple(int(c) for line in file for c in line if c in map(str, range(0, 10)))

def test_solvables():
    test_paths = glob.glob(os.path.join(os.path.dirname(__file__), 'solvable/test??'))
    for test_path in test_paths:
        with open(test_path) as f:
            test = parse_state(f)
        with open(test_path + '_solution') as f:
            solution = parse_state(f)

        check = lambda: nose.tools.assert_equals(solve(test), solution)
        check.description = 'solvable/' + test_path.split('/')[-1]

        yield check

def test_unsolvables():
    test_paths = glob.glob(os.path.join(os.path.dirname(__file__), 'unsolvable/test??'))
    for test_path in test_paths:
        with open(test_path) as f:
            test = parse_state(f)

        check = lambda: nose.tools.assert_equals(solve(test), None)
        check.description = 'unsolvable/' + test_path.split('/')[-1]

        yield check
