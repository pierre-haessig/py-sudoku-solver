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
    all_possibilities = set(range(1,10)) # = {1:9}
    
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
        """remove a set of possibilities
        - returns True if there was strict decrease in
        the size of possibilities set
        - returns False if rm_set has no elements in common with
        possibilities set
        """
        if self.possibilities.isdisjoint(rm_set):
            return False
        else:
            self.possibilities -= rm_set
            assert len(self.possibilities) >= 1
            return True
    # end remove_possibilities
        
    def is_solved(self):
        """is the cell in a solved state, that is
        there is just one possibility"""
        return len(self.possibilities) == 1
    
    def solution(self):
        """returns the cell solution, if available
        else returns None"""
        if self.is_solved():
            return tuple(self.possibilities)[0]
        else:
            return None
    
    def __str__(self):
        """string of the solution, or "-" if Cell is unsolved"""
        sol = self.solution()
        if sol is None:
            return "-"
        else:
            return str(sol)
    
    def __repr__(self):
        sol = self.solution()
        if sol is None:
            return 'Cell((%d,%d))' % self.pos
        else:
            return 'Cell((%d,%d), %s)' % (self.pos + (str(sol),))
        
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
        """get the list of cell in the macro-block (A0,A1)"""
        assert len(block_pos) == 2
        (A0,A1) = block_pos
        print("macro block (%d,%d)" % block_pos)
        return [c for c in self.cells if c.pos[0]//3==A0 and c.pos[1]//3==A1]
    
    def get_set(self,n):
        '''get the list of cell corresponding to set number n.
        This is the generic function to return any type of cell set.
        
        Cell sets are classified as follows :
         * n =  0 to  8  : corresponds to row 0 to 8
         * n =  9 to 17  : corresponds to column 0 to 8
         * n = 18 to 26  : corresponds to macro-block 0 to 8
        '''
        (N0, N1) = self.grid_size
        set_type = n // N0
        assert set_type in set([0,1,2])
        
        if set_type == 0:
            # returns a row
            return self.get_row_set(a0=n)
        
        if set_type == 1:
            # returns a colum
            return self.get_col_set(a1=n-N0)
        
        if set_type == 2:
            # returns a macro block
            block_number = n-N0-N1
            block_pos = (block_number%3, block_number//3)
            return self.get_block_set(block_pos)
    # end get_set
    
    def process_set(self,n):
        """apply the Sudoku exclusion rules to the Cell set n
        (see also Sudoku.get_set(n) )
        returns True if there was some progress in the elimination process"""
        cell_list = self.get_set(n)
        # Find all numbers that are already solved
        solved_numbers = [c.solution() for c in cell_list 
                                       if c.is_solved()]
        print('Solved numbers in set %d : %s' % (n,solved_numbers) )
        # Remove the solved numbers from the set of possibilities
        app = [c.remove_possibilities(set(solved_numbers)) 
               for c in cell_list 
               if not c.is_solved() ]
        nb_progress = len([b for b in app if b])
        print('Number of cells that got some progress : %d' % nb_progress)
        return nb_progress > 0
    
    def process_all_sets(self):
        """apply the Sudoku exclusion rules *once* to each Cell set of the grid
        returns True if there was some progress in the elimination process"""
        progress = False
        for n in range(9+9+9):
            progress |=  self.process_set(n)
        return progress
            
    
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
        s+= '\n\nNumber of solved cells : %d/81' % len([c for c in self.cells if c.is_solved()])
        
        return s
    
    def print_grid(self):
        """displays the grid"""
        print(self)
    
    def print_nb_possibilities(self):
        """displays the number of remaining possibilities in each cell
        a '.' means the cell is solved
        """
        (N0, N1) = self.grid_size          
        print("Number of remaining possibilities :\n")
        for a0 in range(N0):
            if a0 > 0 and a0 % 3 == 0:
                print('')
            str_list = [str(len(c.possibilities)) for c in self.get_row_set(a0)]
            str_list = ['.' if char=='1' else char for char in str_list]
            s  = ''.join(str_list[0:3]) + '  ' +\
                 ''.join(str_list[3:6]) + '  ' +\
                 ''.join(str_list[6:9]) + '  '
            print(s)
        print('\nNumber of solved cells : %d/81' % 
              len([c for c in self.cells if c.is_solved()]))

if __name__ == '__main__':
    print("Sudoku solver program")
    print("-"*21)
    S = Sudoku('sudoku-examples/sudoku-level4-1.txt')
    print(S)
    
    S.process_all_sets()
    S.process_all_sets()
    S.process_all_sets()
    print(S)
    S.print_nb_possibilities()
