#########################
## Connor Nelson, 2016 ##
#########################

import copy
import heapq
from node import Node

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
            node.insert_up(Node(9))
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
            node.insert_up(Node(9))
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
            node.insert_up(Node(9))
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
            node.insert_up(Node(9))
            constraints.insert_left(node.up())
    
    for column in range(9):
        for row in range(9):
            for number in range(9):
                squares[column][row][number] = squares[column][row][number].right()

    # constraints are the major data structure, using 2d linked-list
    # squares provide quick access into a particular square for initial state
    return (constraints, squares)

def inform_constraints(square):
    current = None
    while not current is square:
        if not current:
            current = square

        # remove column
        vertical = current.up() # skip first node for backtrack
        while not vertical is current:
            if not vertical.is_header():
                # remove row
                horizontal = vertical.right() # skip first node for backtrack
                while not horizontal is vertical:
                    horizontal.up().delete_down()
                    horizontal = horizontal.right()
                
            vertical.left().delete_right()
            vertical = vertical.up()
            
        current = current.right()

def uninform_constraints(square):
    current = None
    while not current is square:
        if not current:
            current = square

        # restore column
        vertical = current.down()
        while not vertical is current:
            vertical.right().insert_left(vertical)
            if not vertical.is_header():
                # restore row
                horizontal = vertical.left()
                while not horizontal is vertical:
                    horizontal.down().insert_up(horizontal)
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

def parse_initial_state():
    game_state = []
    for _ in range(9):
        for c in raw_input():
            game_state.append(int(c))
    return tuple(game_state)

def solve_initial_constraints(initial_state, constraints, squares):
    print 'initializing'
    for i, number in enumerate(initial_state):
        if number != 0:
            column = i % 9 + 1
            row = i / 9 + 1
            square = squares[column - 1][row - 1][number - 1]
            inform_constraints(square)

def solve_constraints(constraints, state):
    print 'solving'
    if success(constraints):
        return state
    elif need_backtrack(constraints):
        return False

    constraint = constraints.right() # TODO: use Knuth's optimization of constraint with lowest number
    vertical = constraint.down()
    while not vertical is constraint:
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
        vertical = vertical.down()

    return False # no way to solve the selected constraint from this state        

def print_state(state):
    print TL + HOR * 7 + HOR_T + HOR * 7 + HOR_T + HOR * 7 + TR

    for i, element in enumerate(state):
        if i % 9 == 0 and i != 0:
            print VER
        if i % 27 == 0 and i != 0:
            print VER_L + HOR * 7 + VER_HOR + HOR * 7 + VER_HOR + HOR * 7 + VER_R
        if i % 3 == 0:
            print VER,

        if element == 0:
            print BOX,
        else:
            print element,

    print VER
    print BL + HOR * 7 + HOR_B + HOR * 7 + HOR_B + HOR * 7 + BR

def main():
    initial_state = parse_initial_state()
    constraints, squares = init_constraints()
    solve_initial_constraints(initial_state, constraints, squares)
    solution = solve_constraints(constraints, initial_state)
    if not solution:
        print "This puzzle cannot be solved"
    else:
        print_state(solution)

if __name__ == "__main__":
    main()            
    
    
