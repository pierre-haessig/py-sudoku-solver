#!/usr/bin/python
# -*- coding: UTF-8 -*-
# Pierre Haessig October 2011
""" 
Sudoku Solver
=============

A quick hobby Python program to represent
and (attempt to) solve the classic Sudoku game

see README.rst for more information 
"""

from __future__ import division, print_function


class Cell(object):
    """represents a Sudoku cell"""
    
    # all available possibilities in a the cell :
    all_possibilities = set(range(10)) # = {0:9}
    
    def __init__(self, pos, solution = None):
        """pos = (a0,a1) is the cell position in the grid
        solution : [optional] sets the content of the cell
                   (creates a solved cell)
        """
        assert len(pos) == 2
        self.pos = pos
        self.possibilities = self.all_possibilities.copy()
        
        if solution is not None:
            assert solution in self.all_possibilities
            # remove all possibilities but the solution
            self.remove_possibilities(self.all_possibilities - set([solution]))            
    
    def remove_possibilities(self, rm_set):
        """remove a set of possibilities"""
        self.possibilities -= rm_set
        assert len(self.possibilities) >= 1
        
    def is_solved(self):
        """is the cell in a solved state, that is
        there is just one possibility"""
        return len(self.possibilities) == 1
    
    def __str__(self):
        if self.is_solved():
            return str(tuple(self.possibilities)[0])
        else:
            return "-"
        
class Sudoku(object):
    """represent the Sudoku game"""
    # size of the Sudoku grid
    grid_size = (9,9)
    # size of the subblocks : 
    block_size = (3,3)
    
    def __init__(self, input_game=None):
        """input_game : filename of a file to load the game from
                        if None, Sudoku starts completely unsolved"""
        (N0, N1) = self.grid_size
        
        # Read the input if any
        input_lines = None
        if input_game is not None:
            with open(input_game) as f:
                input_lines = f.readlines()
            
        # All the 9*9 cells are stored in a list : 
        self.cells = []
        # Populate the list:
        for a0 in range(N0):
            for a1 in range(N1):
                sol = None
                if input_lines is not None:
                    sol = input_lines[a0][a1]
                    try:
                       sol = int(sol)
                       #print('(%d,%d) = %d' % (a0, a1, sol))
                    except ValueError:
                        # sol is not a number. Just skip
                        sol = None
                cell = Cell((a0,a1), solution=sol)
                self.cells.append(cell)
    # end __init__
    
    def get_row_set(self, a0):
        """get the list of cells at row a0"""
        return [c for c in self.cells if c.pos[0]==a0]
    
    def get_col_set(self, a1):
        """get the list of cells at column a1"""
        return [c for c in self.cells if c.pos[1]==a1]
    
    def get_block_set(self, block_pos):
        """get the list of cell at block (A0,A1)"""
        return set()
    
    def __str__(self):
        """visual text represtation of the Sudoku grid at current state
        Note : this function assumes block_size == (3,3) 
        and grid width being 9 (that is the usual Sudoku format)
        """
        (N0, N1) = self.grid_size          
        s = "Sudoku grid :\n\n"
        for a0 in range(N0):
            if a0 > 0:
                s+= '\n'
                if a0 % 3 == 0:
                    s+= '\n'
            str_list = [str(c) for c in self.get_row_set(a0)]
            s += ''.join(str_list[0:3]) + '  ' +\
                 ''.join(str_list[3:6]) + '  ' +\
                 ''.join(str_list[6:9]) + '  '
        return s
        

if __name__ == '__main__':
    print("Sudoku solver program")
    print("-"*21)
    S = Sudoku('sudoku-examples/sudoku-level4-1.txt')
    print(S)
