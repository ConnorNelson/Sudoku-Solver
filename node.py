#########################
## Connor Nelson, 2016 ##
#########################

class Node(object):
    
    def __init__(self, number, column = 0, row = 0):
        self._number = number
        self._column = column
        self._row = row
        
        self._prev = self
        self._next = self
        self._up = self
        self._down = self
        
    def __eq__(self, other):
        return self._column == other._column \
            and self._row == other._row \
            and self._number == other._number

    def __str__(self):
        return '[' + str(self._column) + ' ' + str(self._row) + ' ' + str(self._number) + ']'
            
    def is_header(self):
        return column == 0 and row == 0

    def column(self):
        return self._column
        
    def row(self):
        return self._row
            
    def number(self):
        return self._number

    def nxt(self):
        return self._next

    def prev(self):
        return self._prev

    def up(self):
        return self._up

    def down(self):
        return self._down

    def insert_next(self, node):
        node._next = self._next
        self._next._prev = node
        self._next = node
        node._prev = self

    def insert_prev(self, node):
        node._prev = self._prev
        self._prev._next = node
        self._prev = node
        node._next = self

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

    def delete_next(self):
        self._next = self._next._next
        self._next._prev = self

    def delete_prev(self):
        self._prev = self._prev._prev
        self._prev._next = self

    def delete_up(self):
        self._up = self._up._up
        self._up._down = self

    def delete_down(self):
        self._down = self._down._down
        self._down._up = self
