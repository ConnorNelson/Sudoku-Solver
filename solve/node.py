#########################
## Connor Nelson, 2016 ##
#########################

class Node(object):
    
    def __init__(self, number, column = 0, row = 0):
        self._number = number
        self._column = column
        self._row = row
        
        self._left = self
        self._right = self
        self._up = self
        self._down = self
        
    def __eq__(self, other):
        return self._column == other._column \
            and self._row == other._row \
            and self._number == other._number

    def __str__(self):
        return '[' + str(self._column) + ' ' + str(self._row) + ' ' + str(self._number) + ']'
            
    def is_header(self):
        return self._column == 0 and self._row == 0

    def dec_header(self):
        if self.is_header():
            self._number -= 1

    def inc_header(self):
        if self.is_header():
            self._number += 1

    def column(self):
        return self._column
        
    def row(self):
        return self._row
            
    def number(self):
        return self._number

    def right(self):
        return self._right

    def left(self):
        return self._left

    def up(self):
        return self._up

    def down(self):
        return self._down

    def insert_right(self, node):
        node._right = self._right
        self._right._left = node
        self._right = node
        node._left = self

    def insert_left(self, node):
        node._left = self._left
        self._left._right = node
        self._left = node
        node._right = self

    def insert_up(self, node):
        node._up = self._up
        self._up._down = node
        self._up = node
        node._down = self

    def insert_down(self, node):
        node._down = self._down
        self._down._up = node
        self._down = node
        node._up = self

    def delete_right(self):
        self._right = self._right._right
        self._right._left = self

    def delete_left(self):
        self._left = self._left._left
        self._left._right = self

    def delete_up(self):
        self._up = self._up._up
        self._up._down = self

    def delete_down(self):
        self._down = self._down._down
        self._down._up = self
