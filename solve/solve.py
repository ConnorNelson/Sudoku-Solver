#########################
## Connor Nelson, 2016 ##
#########################

import time
from node import Node

# debug info
DEBUG = False
total_backtracks = 0

# shapes/lines for fancy printing
TL = u'\u250F'
TR = u'\u2513'
BL = u'\u2517'
BR = u'\u251B'
HOR = u'\u2501'
HOR_T = u'\u2533'
HOR_B = u'\u253B'
VER = u'\u2503'
VER_L = u'\u2523'
VER_R = u'\u252B'
VER_HOR = u'\u254B'
BOX = u'\u25A1'

def debug_time(function):
    def timed(*args, **kw):
        start = time.time()
        result = function(*args, **kw)
        if DEBUG:
            print function.__name__, "took (seconds):", '{0:.3f}'.format(time.time() - start)
        return result
    return timed

def debug_print_info():
    if DEBUG:
        print "total backtracks:", total_backtracks

@debug_time
def init_constraints():
    constraints = Node(-1, -1, -1)
    squares = []

    # some number in every column/row
    for column in range(1, 10):
        rows = []
        for row in range(1, 10):
            numbers = []
            node = Node(1, column, row)
            numbers.append(node)
            for number in range(2, 10):
                node.insert_up(Node(number, column, row))
                numbers.append(node.up())
            node.insert_up(Node(9)) # all constraints can be solved by 9 squares
            constraints.insert_left(node.up())
            rows.append(numbers)
        squares.append(rows)

    # every number in every column (some row in every number/column)
    for number in range(1, 10):
        for column in range(1, 10):
            node = Node(number, column, 1)
            squares[column - 1][0][number - 1].insert_right(node)
            squares[column - 1][0][number - 1] = node
            for row in range(2, 10):
                node.insert_up(Node(number, column, row))
                squares[column - 1][row - 1][number - 1].insert_right(node.up())
                squares[column - 1][row - 1][number - 1] = node.up()
            node.insert_up(Node(9)) # all constraints can be solved by 9 squares
            constraints.insert_left(node.up())

    # every number in every row (some column in every number/row)
    for number in range(1, 10):
        for row in range(1, 10):
            node = Node(number, 1, row)
            squares[0][row - 1][number - 1].insert_right(node)
            squares[0][row - 1][number - 1] = node
            for column in range(2, 10):
                node.insert_up(Node(number, column, row))
                squares[column - 1][row - 1][number - 1].insert_right(node.up())
                squares[column - 1][row - 1][number - 1] = node.up()
            node.insert_up(Node(9)) # all constraints can be solved by 9 squares
            constraints.insert_left(node.up())

    # every number in every block
    for number in range (1, 10):
        for block in range(9):
            base_column = (3 * block) % 9 + 1
            base_row = 3 * (block / 3) + 1
            node = Node(number, base_column, base_row)
            squares[base_column - 1][base_row - 1][number - 1].insert_right(node)
            squares[base_column - 1][base_row - 1][number - 1] = node
            for block_row in range(3):
                for block_column in range(3):
                    if block_column == 0 and block_row == 0:
                        continue # first node already created
                    column = base_column + block_column
                    row = base_row + block_row
                    node.insert_up(Node(number, column, row))
                    squares[column - 1][row - 1][number - 1].insert_right(node.up())
                    squares[column - 1][row - 1][number - 1] = node.up()
            node.insert_up(Node(9)) # all constraints can be solved by 9 squares
            constraints.insert_left(node.up())

    for column in range(9):
        for row in range(9):
            for number in range(9):
                squares[column][row][number] = squares[column][row][number].right()

    return constraints

def inform_constraints(square):
    current = None
    while current is not square:
        if not current:
            current = square

        # remove column
        vertical = current.up() # skip first node for backtrack
        while vertical is not current:
            if not vertical.is_header():
                # remove row
                horizontal = vertical.right() # skip first node for backtrack
                while horizontal is not vertical:
                    horizontal.up().delete_down()

                    # update the header
                    header = horizontal.up()
                    while not header.is_header():
                        header = header.up()
                    header.dec_header()

                    horizontal = horizontal.right()

            vertical.left().delete_right()
            vertical = vertical.up()

        current = current.right()

def uninform_constraints(square):
    current = None
    while current is not square:
        if not current:
            current = square

        # restore column
        vertical = current.down()
        while vertical is not current:
            vertical.right().insert_left(vertical)
            if not vertical.is_header():
                # restore row
                horizontal = vertical.left()
                while horizontal is not vertical:
                    horizontal.down().insert_up(horizontal)

                    # update the header
                    header = horizontal.down()
                    while not header.is_header():
                        header = header.down()
                    header.inc_header()

                    horizontal = horizontal.left()

            vertical = vertical.down()

        current = current.left()

def success(constraints):
    return constraints.right() is constraints

def need_backtrack(constraints):
    constraint = constraints
    while True:
        constraint = constraint.right()
        if constraint.number() == 0:
            return True
        if constraint is constraints:
            return False

def update_state(state, number, column, row):
    index = 9 * (row - 1) + (column - 1)
    return state[:index] + (number,) + state[index + 1:]

@debug_time
def solve_initial_constraints(initial_state, constraints):
    for i, number in enumerate(initial_state):
        if number != 0:
            column = i % 9 + 1
            row = i / 9 + 1
            square = None
            constraint = constraints.right()
            while constraint is not constraints and square is None:
                vertical = constraint.down()
                while vertical is not constraint and square is None:
                    if vertical.number() == number \
                       and vertical.column() == column \
                       and vertical.row() == row:
                        square = vertical
                    vertical = vertical.down()
                constraint = constraint.right()
            if (square):
                inform_constraints(square)
            else:
                return False
    return True

def solve_constraints(constraints, state):
    if success(constraints):
        return state
    if need_backtrack(constraints):
        return False

    constraint = constraints.right()
    optimal_constraint = constraint
    while constraint is not constraints:
        if constraint.number() < optimal_constraint.number():
            optimal_constraint = constraint
        constraint = constraint.right()

    vertical = optimal_constraint.down()
    while vertical is not optimal_constraint:
        inform_constraints(vertical)
        solution = solve_constraints(constraints, state)
        if solution:
            number = vertical.number()
            column = vertical.column()
            row = vertical.row()
            return update_state(solution, number, column, row)
        else:
            # need to backtrack
            uninform_constraints(vertical)
            if DEBUG:
                global total_backtracks
                total_backtracks += 1
        vertical = vertical.down()

    return False # no way to solve the selected constraint from this state

@debug_time
def solve(initial_state):
    constraints = init_constraints()
    solvable = solve_initial_constraints(initial_state, constraints)
    if solvable:
        @debug_time
        def complete_solve_constraints(constraints, initial_state):
            return solve_constraints(constraints, initial_state)
        solution = complete_solve_constraints(constraints, initial_state)
        return solution
    else:
        return None

def main():
    initial_state = []
    for _ in range(9):
        for c in raw_input():
            initial_state.append(int(c))
    initial_state = tuple(initial_state)

    solution = solve(initial_state)

    if solution:
        for row in range(0, 9 ** 2, 9):
            print ''.join(map(str, solution[row:row + 9]))
    else:
        print "This puzzle cannot be solved"

    debug_print_info()

if __name__ == '__main__':
    main()


